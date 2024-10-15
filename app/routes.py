from flask import Blueprint, request
from constants import CREATE_URL, DELETE_URL, GET_URL, UPDATE_URL
from controllers.service_controller import ServiceController
from controllers.user_controller import UserController

api = Blueprint("api", __name__)

# USER ROUTES


@api.route(CREATE_URL + "/user", methods=["POST"])
def create_user():
    """POST /api/v1/create/user - create user"""
    data = request.get_json()

    return UserController.post(data=data)


@api.route(GET_URL + "/users", methods=["GET"])
def get_users():
    """GET /api/v1/get/users - query all users"""

    return UserController.get()


@api.route(GET_URL + "/user", methods=["GET"])
def get_user():
    """GET /api/v1/get/user?id=guid - query user by guid"""

    guid = request.args.get("id")

    return UserController.get(guid=guid)


@api.route(GET_URL + "/search/user", methods=["GET"])
def search_user():
    """GET /api/v1/search/user?login=login - query user by login"""

    data = {
        "login": request.args.get("login"),
        "email": request.args.get("email"),
        "phone_number": request.args.get("phone_number"),
        "account_type": request.args.get("account_type"),
        "is_active": request.args.get("is_active"),
    }

    for key in list(data.keys()):
        if data[key] is None:
            del data[key]

    return UserController.search(data=data)


@api.route(UPDATE_URL + "/user", methods=["PUT"])
def update_user():
    """PUT /api/v1/update/user?id=guid - update user by guid"""

    guid = request.args.get("id")
    data = request.get_json()

    return UserController.put(guid=guid, data=data)


@api.route(UPDATE_URL + "/pass/user", methods=["PUT"])
def update_password():
    """PUT /api/v1/update/pass/user?id=guid - update user password by guid"""

    guid = request.args.get("id")
    data = request.get_json()

    return UserController.change_password(guid=guid, data=data)


@api.route(DELETE_URL + "/user", methods=["DELETE"])
def delete_user():
    """DELETE /api/v1/delete/user?id=guid - delete user by guid"""

    guid = request.args.get("id")

    return UserController.delete(guid=guid)


# SERVICE ROUTES


@api.route(CREATE_URL + "/service", methods=["POST"])
def create_service():
    """POST /api/v1/create/service - create service"""
    data = request.get_json()

    return ServiceController.post(data=data)


@api.route(GET_URL + "/services", methods=["GET"])
def get_services():
    """GET /api/v1/get/services - query all services"""

    return ServiceController.get()


@api.route(GET_URL + "/service", methods=["GET"])
def get_service():
    """GET /api/v1/get/service?id=guid - query service by guid"""

    guid = request.args.get("id")

    return ServiceController.get(guid=guid)


@api.route(UPDATE_URL + "/service", methods=["PUT"])
def update_service():
    """PUT /api/v1/update/service?id=guid - update service by guid"""

    guid = request.args.get("id")
    data = request.get_json()

    return ServiceController.put(guid=guid, data=data)


@api.route(DELETE_URL + "/service", methods=["DELETE"])
def delete_service():
    """DELETE /api/v1/delete/service?id=guid - delete service by guid"""

    guid = request.args.get("id")

    return ServiceController.delete(guid=guid)


@api.route(GET_URL + "/search/service", methods=["GET"])
def search_service():
    """GET /api/v1/search/service?name=name - query service by name"""

    data = {
        "name": request.args.get("name"),
        "actual_state": request.args.get("actual_state"),
        "status": request.args.get("status"),
        "address": request.args.get("address"),
    }

    for key in list(data.keys()):
        if data[key] is None:
            del data[key]

    return ServiceController.search(data=data)
