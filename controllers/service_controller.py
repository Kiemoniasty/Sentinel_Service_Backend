from flask import jsonify

from enums.sentinel_enums import Response, Status


class ServiceController:

    def post(self=None, data=None):

        from models.settings import Settings
        from models.service import Service
        from app.flask import db

        if "status" in data:
            for item in Status:
                if item.value == data["status"]:
                    data["status"] = item.name

        if "actual_state" in data:
            for item in Response:
                if item.value == data["actual_state"]:
                    data["actual_state"] = item.name

        new_setting = Settings(
            guid=data.get("setting_guid"),
            status=data["status"],
            address=data["address"],
            frequency=int(data["frequency"]),
            response_time=int(data["response_time"]),
            number_of_samples=int(data["number_of_samples"]),
        )

        db.session.add(new_setting)
        db.session.commit()

        new_service = Service(
            guid=data.get("guid"),
            name=data["name"],
            actual_state=data["actual_state"],
            setting_guid=new_setting.guid,
        )

        db.session.add(new_service)
        db.session.commit()

        return jsonify({"message": "Service created successfully"}), 201

    def get(self=None, guid=None):

        from models.service import Service
        from models.settings import Settings

        if guid:
            query = Service.query.filter_by(guid=guid)
            subquery = Settings.query.filter_by(guid=query.setting_guid)
        else:
            query = Service.query.all()
            subquery = Settings.query.all()

        result = []
        for item in query:
            for subitem in subquery:
                if item.setting_guid == subitem.guid:
                    result.append(
                        {
                            "guid": item.guid,
                            "name": item.name,
                            "setting": {
                                "guid": subitem.guid,
                                "status": subitem.status.value,
                                "address": subitem.address,
                                "frequency": subitem.frequency,
                                "response_time": subitem.response_time,
                                "number_of_samples": subitem.number_of_samples,
                            },
                            "actual_state": item.actual_state.value,
                        }
                    )

        if not result:
            return jsonify({"message": "No service found"}), 404
        else:
            return jsonify(result), 200

    def put(self=None, guid=None, data=None):

        if "status" in data:
            for item in Status:
                if item.value == data["status"]:
                    data["status"] = item.name

        if "actual_state" in data:
            for item in Response:
                if item.value == data["actual_state"]:
                    data["actual_state"] = item.name

        from models.service import Service
        from models.settings import Settings
        from app.flask import db

        service = Service.query.filter_by(guid=guid)
        settings = Settings.query.filter_by(guid=service.setting_guid)

        if not service:
            return jsonify({"message": "No service found"}), 404

        for item in service:
            if "name" in data:
                item.name = data["name"]
            if "actual_state" in data:
                item.actual_state = data["actual_state"]

        for subitem in settings:
            if "status" in data:
                subitem.status = data["status"]
            if "address" in data:
                subitem.address = data["address"]
            if "frequency" in data:
                subitem.frequency = data["frequency"]
            if "response_time" in data:
                subitem.response_time = data["response_time"]
            if "number_of_samples" in data:
                subitem.number_of_samples = data["number_of_samples"]

        db.session.commit()

        return {"message": "Service updated successfully"}, 200

    def delete(self=None, guid=None):

        from models.service import Service
        from models.settings import Settings
        from app.flask import db

        service = Service.query.filter_by(guid=guid)

        if not service:
            return jsonify({"message": "No service found"}), 404
        else:
            settings = Settings.query.filter_by(guid=service.setting_guid)
            db.session.delete(service)
            db.session.delete(settings)
            db.session.commit()
            return jsonify({"message": "Service deleted successfully"}), 200

    def search(self=None, data=None):

        if "status" in data:
            for item in Status:
                if item.value == data["status"]:
                    data["status"] = item.name
                else:
                    del data["status"]

        if "actual_state" in data:
            for item in Response:
                if item.value == data["actual_state"]:
                    data["actual_state"] = item.name
                else:
                    del data["actual_state"]

        from models.service import Service
        from models.settings import Settings

        if data:
            query = Service.query.filter(
                Service.name.like(f"%{data['name']}%"),
                Service.actual_state == data["actual_state"],
            )
            reverse_query = Settings.query.filter(
                Settings.status == data["status"] if "status" in data else True,
                Settings.address.like(f"%{data['address']}%"),
            )

            result = []
            for service in query:
                for setting in reverse_query:
                    if service.setting_guid == setting.guid:
                        result.append(
                            {
                                "guid": service.guid,
                                "name": service.name,
                                "setting": {
                                    "guid": setting.guid,
                                    "status": setting.status.value,
                                    "address": setting.address,
                                    "frequency": setting.frequency,
                                    "response_time": setting.response_time,
                                    "number_of_samples": setting.number_of_samples,
                                },
                                "actual_state": service.actual_state.value,
                            }
                        )

        if not result:
            return jsonify({"message": "No service found"}), 404
        else:
            return jsonify(result), 200
