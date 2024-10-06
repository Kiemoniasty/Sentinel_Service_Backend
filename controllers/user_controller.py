from flask import jsonify
from flask_restful import Resource

# from app.flask import api


class UserController(Resource):
    def get(
        self=None,
        guid=None,
        login=None,
        email=None,
        phone_number=None,
        account_type=None,
        is_active=None,
    ):

        filter_list = []
        if guid:
            filter_list.append(f"guid='{guid}'")
        if login:
            filter_list.append(f"login='{login}'")
        if email:
            filter_list.append(f"email='{email}'")
        if phone_number:
            filter_list.append(f"phone_number='{phone_number}'")
        if account_type:
            filter_list.append(f"account_type='{account_type}'")
        if is_active:
            filter_list.append(f"is_active={is_active}")

        filter_collection = ""

        for item in filter_list:
            if item == filter_list[0]:
                filter_collection = item
            else:
                filter_collection += "," + item

        from models.user import User

        if filter_collection:
            query = User.query.filter(filter_collection).first()
        else:
            query = User.query.all()

        if not query:
            return jsonify({"message": "No user found"})
        else:
            result = []
            for item in query:
                result.append(
                    {
                        "guid": item.guid,
                        "login": item.login,
                        "email": item.email,
                        "phone_number": item.phone_number,
                        "account_type": item.account_type,
                        "is_active": item.is_active,
                    }
                )
        return jsonify(result)


# api.add_resource(UserController, "/users", "/user/<string:guid>")

#     def post(self):
#         data = request.get_json()
#         conn = PostgresTools.userdb_connector()
#         cursor = conn.cursor()

#         cursor.execute(
#             """INSERT INTO users (guid, login, email, password, phone_number, account_type, is_active)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)""",
#             (
#                 data["guid"],
#                 data["login"],
#                 data["email"],
#                 data["password"],
#                 data["phone_number"],
#                 data["account_type"],
#                 data["is_active"],
#             ),
#         )
#         conn.commit()
#         conn.close()
#         return jsonify({"message": "User created successfully"}), 201

#     def put(self, guid):
#         data = request.get_json()
#         conn = PostgresTools.userdb_connector()
#         cursor = conn.cursor()

#         cursor.execute(
#             """UPDATE users
#             SET login = %s, email = %s, password = %s, phone_number = %s, account_type = %s, is_active = %s
#             WHERE guid = %s""",
#             (
#                 data["login"],
#                 data["email"],
#                 data["password"],
#                 data["phone_number"],
#                 data["account_type"],
#                 data["is_active"],
#                 guid,
#             ),
#         )
#         conn.commit()
#         conn.close()
#         return jsonify({"message": "User updated successfully"})

#     def delete(self, guid):
#         conn = PostgresTools.userdb_connector()
#         cursor = conn.cursor()

#         cursor.execute("DELETE FROM users WHERE guid = %s", (guid,))
#         conn.commit()
#         conn.close()
#         return "", 204


# # Add User Resource to the API
# # api.add_resource(User, "/users", "/users/<string:guid>")
