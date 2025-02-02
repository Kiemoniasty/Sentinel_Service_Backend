"""Controller for user instance"""

from flask import jsonify
from flask_jwt_extended import create_access_token
import constants
from controllers.user_tools import UserTools
from databases.influxdb_tools import InfluxTools
from databases.postgres_tools import PostgresTools
from enums.user_enums import AccountType


class UserController:
    """Controller for user instance"""

    def post(self=None, data=None):
        """Create a new user in the database"""

        if "account_type" in data:
            data["account_type"] = UserTools.valid_account_type(
                account_type=data["account_type"]
            )

        if "is_active" in data:
            data["is_active"] = UserTools.valid_is_active(is_active=data["is_active"])
            if data["is_active"] is None:
                del data["is_active"]

        from models.user import User

        new_user = User(
            guid=data.get("guid"),
            login=data["login"],
            password=UserTools.hash_password(password=data["password"]),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            account_type=(
                data.get("account_type")
                if "account_type" in data
                else AccountType.USER.name
            ),
            is_active=data.get("is_active"),
        )

        message = UserTools.valid_new_user(data=data)

        if message:
            return jsonify({"message": message}), 409
        else:
            PostgresTools.write_data(data=new_user)
            content = constants.USR_NEW1 + new_user.login + constants.USR_NEW2
            InfluxTools.write_log(content)

            return jsonify({"message": "User created successfully"}), 201

    def get(self=None, guid=None):
        """Query user/s from database depending on the guid if provided"""

        from models.user import User

        if guid:
            query = User.query.filter_by(guid=guid)
        else:
            query = User.query.all()

        result = UserTools.user_to_list(data=query)

        if not result:
            return jsonify({"message": "No user found"}), 404
        else:
            return jsonify(result), 200

    def put(self=None, guid=None, data=None):
        """Update user in the database"""
        from models.user import User
        from app.flask import db

        user = User.query.filter_by(guid=guid).first()
        if not user:
            return jsonify({"message": "No user found"}), 404

        if "account_type" in data:
            data["account_type"] = UserTools.valid_account_type(
                account_type=data["account_type"]
            )
        if "is_active" in data:
            data["is_active"] = UserTools.valid_is_active(is_active=data["is_active"])

        if "login" in data:
            user.login = data["login"]
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = UserTools.hash_password(password=data["password"])
        if "phone_number" in data:
            user.phone_number = data["phone_number"]
        if "account_type" in data:
            user.account_type = data["account_type"]
        if "is_active" in data:
            user.is_active = data["is_active"]

        db.session.commit()

        content = constants.USR_UPD1 + user.login + constants.USR_UPD2
        InfluxTools.write_log(content)

        return jsonify({"message": "User updated successfully"}), 200

    def delete(self=None, guid=None):
        """Delete user from the database"""
        from models.user import User

        user = User.query.filter_by(guid=guid).first()
        if not user:
            return jsonify({"message": "No user found"}), 404
        elif user.is_active:
            return jsonify({"message": "User is active"}), 409
        else:
            PostgresTools.delete_data(data=user)

            content = constants.USR_DEL1 + user.login + constants.USR_DEL2
            InfluxTools.write_log(content)

            return jsonify({"message": "User deleted successfully"}), 200

    def search(self=None, data=None):
        """Search user in the database"""

        from models.user import User

        if "is_active" in data:
            data["is_active"] = UserTools.valid_is_active(is_active=data["is_active"])
            if data["is_active"] is None:
                del data["is_active"]

        if "account_type" in data:
            data["account_type"] = UserTools.valid_account_type(
                account_type=data["account_type"]
            )

        if data:
            query = User.query.filter(
                User.login.ilike(f"%{data['login']}%") if "login" in data else True,
                User.email.ilike(f"%{data['email']}%") if "email" in data else True,
                (
                    User.phone_number.ilike(f"%{data['phone_number']}%")
                    if "phone_number" in data
                    else True
                ),
                (
                    User.account_type == data["account_type"]
                    if "account_type" in data
                    else True
                ),
                (User.is_active == data["is_active"] if "is_active" in data else True),
            )
        else:
            query = User.query.all()

        result = UserTools.user_to_list(data=query)

        if not result:
            return jsonify({"message": "No user found"}), 404
        else:
            return jsonify(result), 200

    def login(self=None, data=None):
        """Login user"""
        from models.user import User

        user = User.query.filter_by(login=data["login"]).first()

        if not user:
            return jsonify({"message": "Invalid login or password"}), 401
        elif not UserTools.check_password(
            hashed_pass=user.password, password=data["password"]
        ):
            return jsonify({"message": "Invalid login or password"}), 401
        else:
            access_token = create_access_token(
                identity=user.guid, additional_claims={"role": user.account_type.value}
            )
            return jsonify({"access_token": access_token}), 200

    def change_password(self=None, guid=None, data=None):
        """Change user password"""
        from models.user import User
        from app.flask import db

        user = User.query.filter_by(guid=guid).first()
        new_password = data.get("new_password")

        if not user:
            return jsonify({"message": "Invalid login or password"}), 401

        if not UserTools.check_password(
            hashed_pass=user.password, password=data["password"]
        ):
            return jsonify({"message": "Invalid login or password"}), 401
        else:
            user.password = UserTools.hash_password(password=new_password)
            db.session.commit()
            return jsonify({"message": "Password updated successfully"}), 200

    def get_logs(self=None, sort=None, page=None, date=None):
        """Query logs from the database"""

        result = InfluxTools.query_app_logs()
        result = sorted(
            result,
            key=lambda x: x["time_stamp"],
            reverse=True if sort == "desc" else False,
        )
        if date:
            result = [
                item for item in result if item["time_stamp"].split("T")[0] == date
            ]

        if page:
            result = result[int(page) * 30 : (int(page) + 1) * 30]

        if not result:
            return jsonify({"message": "No logs found"}), 404
        else:
            return jsonify(result), 200
