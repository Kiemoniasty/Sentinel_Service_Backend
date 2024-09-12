from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from dotenv import load_dotenv

from databases.postgres_tools import PostgresTools

load_dotenv()


class User(Resource):
    def get(self, guid=None):
        conn = PostgresTools.userdb_connector()
        cursor = conn.cursor()

        if guid:
            cursor.execute("SELECT * FROM users WHERE guid = %s", (guid,))
            user = cursor.fetchone()
            if user:
                result = {
                    "guid": user[0],
                    "login": user[1],
                    "email": user[2],
                    "password": user[3],
                    "phone_number": user[4],
                    "account_type": user[5],
                    "is_active": user[6],
                }
                conn.close()
                return jsonify(result)
            else:
                conn.close()
                return jsonify({"message": "User not found"}), 404
        else:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            result = []
            for user in users:
                result.append(
                    {
                        "guid": user[0],
                        "login": user[1],
                        "email": user[2],
                        "password": user[3],
                        "phone_number": user[4],
                        "account_type": user[5],
                        "is_active": user[6],
                    }
                )
            conn.close()
            return jsonify(result)

    def post(self):
        data = request.get_json()
        conn = PostgresTools.userdb_connector()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO users (guid, login, email, password, phone_number, account_type, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                data["guid"],
                data["login"],
                data["email"],
                data["password"],
                data["phone_number"],
                data["account_type"],
                data["is_active"],
            ),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "User created successfully"}), 201

    def put(self, guid):
        data = request.get_json()
        conn = PostgresTools.userdb_connector()
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE users
            SET login = %s, email = %s, password = %s, phone_number = %s, account_type = %s, is_active = %s
            WHERE guid = %s""",
            (
                data["login"],
                data["email"],
                data["password"],
                data["phone_number"],
                data["account_type"],
                data["is_active"],
                guid,
            ),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "User updated successfully"})

    def delete(self, guid):
        conn = PostgresTools.userdb_connector()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE guid = %s", (guid,))
        conn.commit()
        conn.close()
        return "", 204


# Add User Resource to the API
# api.add_resource(User, "/users", "/users/<string:guid>")
