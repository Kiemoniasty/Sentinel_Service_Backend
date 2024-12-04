"""Collection of methods for ServiceController"""

from flask import jsonify
import constants
from controllers.service_tools import ServiceTools
from databases.influxdb_tools import InfluxTools
from databases.postgres_tools import PostgresTools
from enums.sentinel_enums import Status


class ServiceController:
    """ServiceController class to manage services routes"""

    def post(self=None, data=None):
        """Create a new service and its settings in database"""

        setting = data.get("settings", {})

        if "status" in setting:
            setting["status"] = ServiceTools.valid_status(status=setting["status"])

        if "actual_state" in data:
            data["actual_state"] = ServiceTools.valid_actual_state(
                actual_state=data["actual_state"]
            )

        if not "name" in data:
            return jsonify({"message": "Name is required"}), 405
        if not "address" in setting:
            return jsonify({"message": "Address is required"}), 405

        from models.settings import Settings
        from models.service import Service

        new_setting = Settings(
            guid=setting.get("guid"),
            status=setting.get("status"),
            address=setting["address"],
            frequency=int(setting.get("frequency")),
            response_time=int(setting.get("response_time")),
            number_of_samples=int(setting.get("number_of_samples")),
        )

        # write data to Postgres
        PostgresTools.write_data(data=new_setting)

        new_service = Service(
            guid=data.get("guid"),
            name=data["name"],
            actual_state=data["actual_state"],
            setting_guid=new_setting.guid,
        )

        # write data to Postgres
        PostgresTools.write_data(data=new_service)

        # create bucket in InfluxDB
        InfluxTools.create_bucket(name=new_service.guid)
        # InfluxTools.delete_bucket(name=new_service.guid)

        # create task in scheduler
        from app.flask import state_checker

        if new_setting.status.name == Status.ACTIVE.name:
            state_checker.schedule_task(new_service, new_setting)
            content = (
                constants.SCHD_NEW1
                + str(new_service.name)
                + constants.SCHD_NEW2
                + str(new_service.guid)
                + constants.SCHD_NEW3
            )
            InfluxTools.write_log(content)

        return jsonify({"message": "Service created successfully"}), 201

    def get(self=None, guid=None):
        """Query service/s and its settings from database depending on the guid if provided"""
        from models.settings import Settings
        from models.service import Service

        query = None
        subquery = None

        if guid:
            query = Service.query.filter_by(guid=guid)

            if query:
                setting = query.first()
                subquery = Settings.query.filter_by(guid=setting.setting_guid)

        else:
            query = Service.query.all()
            subquery = Settings.query.all()

        result = ServiceTools.service_to_list(service=query, settings=subquery)

        if not result:
            return jsonify({"message": "No service found"}), 404
        else:
            return jsonify(result), 200

    def put(self=None, guid=None, data=None):
        """Update services and its settings in the database"""

        from models.service import Service

        service = Service.query.filter_by(guid=guid).first()

        if not service:
            return jsonify({"message": "No service found"}), 404
        else:
            PostgresTools.update_service(guid=guid, data=data)

        # changes in scheduler
        from models.settings import Settings
        from app.flask import state_checker

        settings = Settings.query.filter_by(guid=service.setting_guid).first()

        if settings.status.name == Status.ACTIVE.name:
            state_checker.stop_task_by_tag(service.guid, service.name)
            state_checker.schedule_task(service, settings)

            content = (
                constants.SCHD_RES1
                + str(service.name)
                + constants.SCHD_RES2
                + str(service.guid)
                + constants.SCHD_RES3
            )
        else:
            state_checker.stop_task_by_tag(service.guid, service.name)

            content = (
                constants.SCHD_STOP1
                + str(service.name)
                + constants.SCHD_STOP2
                + str(service.guid)
                + constants.SCHD_STOP3
            )

        InfluxTools.write_log(content)

        return {"message": "Service updated successfully"}, 200

    def delete(self=None, guid=None):
        """Delete services and its settings from the database"""
        from models.settings import Settings
        from models.service import Service
        from app.flask import state_checker

        service = Service.query.filter_by(guid=guid).first()
        settings = Settings.query.filter_by(guid=service.setting_guid).first()

        if not service:
            return jsonify({"message": "No service found"}), 404
        elif settings.status == Status.ACTIVE.name:
            return jsonify({"message": "Service is active"}), 400
        else:
            PostgresTools.delete_data(data=service)
            PostgresTools.delete_data(data=settings)
            InfluxTools.delete_bucket(name=guid)
            state_checker.stop_task_by_tag(guid, service.name)

            content = (
                constants.SCHD_STOP1
                + str(service.name)
                + constants.SCHD_STOP2
                + str(service.guid)
                + constants.SCHD_STOP3
            )
            InfluxTools.write_log(content)

            return jsonify({"message": "Service deleted successfully"}), 200

    def search(self=None, data=None):
        """Search service in the database"""

        if "status" in data:
            data["status"] = ServiceTools.valid_status(status=data["status"])

        if "actual_state" in data:
            data["actual_state"] = ServiceTools.valid_actual_state(
                actual_state=data["actual_state"]
            )

        from models.settings import Settings
        from models.service import Service

        result = []
        if data:
            query = Service.query.filter(
                (Service.name.ilike(f"%{data['name']}%") if "name" in data else True),
                (
                    Service.actual_state == data["actual_state"]
                    if "actual_state" in data
                    else True
                ),
            )
            reverse_query = Settings.query.filter(
                Settings.status == data["status"] if "status" in data else True,
                (
                    Settings.address.ilike(f"%{data['address']}%")
                    if "address" in data
                    else True
                ),
            )

            result = ServiceTools.query_to_list(service=query, settings=reverse_query)

        if not result:
            return jsonify({"message": "No service found"}), 404
        else:
            return jsonify(result), 200
