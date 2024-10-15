"""Controller for user instance"""

from flask import jsonify
from enums.user_enums import AccountType


class UserController:
    """Controller for user instance"""

    def post(self=None, data=None):
        """Create a new user in the database"""

        if "account_type" in data:
            for item in AccountType:
                if item.value == data["account_type"]:
                    data["account_type"] = item.name

        from models.user import User
        from app.flask import db

        new_user = User(
            guid=data.get("guid"),
            login=data["login"],
            password=data["password"],
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            account_type=data.get("account_type", AccountType.USER.name),
            is_active=data.get("is_active"),
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201

    def get(self=None, guid=None):
        """Query user/s from database depending on the guid if provided"""

        from models.user import User

        if guid:
            query = User.query.filter_by(guid=guid)
        else:
            query = User.query.all()

        result = []
        for item in query:
            result.append(
                {
                    "guid": item.guid,
                    "login": item.login,
                    "email": item.email,
                    "phone_number": item.phone_number,
                    "account_type": item.account_type.value,
                    "is_active": item.is_active,
                }
            )
        if not result:
            return jsonify({"message": "No user found"}), 404
        else:
            return jsonify(result), 200

    def put(self=None, guid=None, data=None):
        """Update user in the database"""
        from models.user import User
        from app.flask import db

        user = User.query.filter_by(guid=guid)
        if not user:
            return jsonify({"message": "No user found"}), 404

        if "account_type" in data:
            for item in AccountType:
                if item.value == data["account_type"]:
                    data["account_type"] = item.name

        for item in user:
            if "login" in data:
                item.login = data["login"]
            if "email" in data:
                item.email = data["email"]
            if "phone_number" in data:
                item.phone_number = data["phone_number"]
            if "account_type" in data:
                item.account_type = data["account_type"]
            if "is_active" in data:
                item.is_active = data["is_active"]

        db.session.commit()

        return jsonify({"message": "User updated successfully"}), 200

    def delete(self=None, guid=None):
        """Delete user from the database"""
        from models.user import User
        from app.flask import db

        user = User.query.filter_by(guid=guid).first()
        if not user:
            return jsonify({"message": "No user found"}), 404
        else:
            db.session.delete(user)
            db.session.commit()

            return jsonify({"message": "User deleted successfully"}), 200

    def search(self=None, data=None):
        """Search user in the database"""

        from models.user import User

        if "is_active" in data:
            if data["is_active"].lower() == "active":
                data["is_active"] = True
            elif data["is_active"].lower() == "inactive":
                data["is_active"] = False
            else:
                del data["is_active"]

        if "account_type" in data:
            for item in AccountType:
                if item.value == data["account_type"]:
                    data["account_type"] = item.name

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

        result = []
        for item in query:
            result.append(
                {
                    "guid": item.guid,
                    "login": item.login,
                    "email": item.email,
                    "phone_number": item.phone_number,
                    "account_type": item.account_type.value,
                    "is_active": item.is_active,
                }
            )

        if not result:
            return jsonify({"message": "No user found"}), 404
        else:
            return jsonify(result), 200

    def change_password(self=None, guid=None, data=None):
        """Change user password"""
        from models.user import User
        from app.flask import db

        user = User.query.filter_by(guid=guid)

        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not user:
            return jsonify({"message": "No user found"}), 404

        if user.password != current_password:
            return jsonify({"message": "Invalid password"}), 401
        else:
            user.password = new_password
            db.session.commit()
            return jsonify({"message": "Password updated successfully"}), 200
