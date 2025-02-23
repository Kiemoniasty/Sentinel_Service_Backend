"""Collection of routes for the API"""

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from constants import BASE_URL
from controllers.service_controller import ServiceController
from controllers.user_controller import UserController
from app.route_tools import role_required


api = Blueprint("api", __name__)

# IS ALIVE ROUTE


@api.route("/health", methods=["GET"])
def is_alive():
    """GET /health - check if the service is alive"""
    return {"status": "OK"}, 200


# USER ROUTES


@api.route(BASE_URL + "/user", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_user():
    """POST /api/v1/user - create user"""
    data = request.get_json()
    return UserController.post(data=data)


@api.route(BASE_URL + "/users", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_users():
    """GET /api/v1/users - query all users"""
    return UserController.get()


@api.route(BASE_URL + "/user", methods=["GET"])
@jwt_required()
def get_user():
    """GET /api/v1/user?id=guid - query user by guid"""
    guid = request.args.get("id")
    return UserController.get(guid=guid)


@api.route(BASE_URL + "/whoami", methods=["GET"])
@jwt_required()
def whoami():
    """GET /api/v1/whoami - query user by guid"""
    guid = get_jwt_identity()
    return UserController.get(guid=guid)


@api.route(BASE_URL + "/searchUser", methods=["GET"])
@jwt_required()
def search_user():
    """GET /api/v1/searchUser?login=login - query user by login"""
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


@api.route(BASE_URL + "/user", methods=["PUT"])
@jwt_required()
@role_required("admin")
def update_user():
    """PUT /api/v1/user?id=guid - update user by guid"""
    guid = request.args.get("id")
    data = request.get_json()
    return UserController.put(guid=guid, data=data)


@api.route(BASE_URL + "/pass", methods=["PUT"])
@jwt_required()
def update_password():
    """PUT /api/v1/pass?id=guid - update user password by guid"""
    guid = request.args.get("id")
    data = request.get_json()
    return UserController.change_password(guid=guid, data=data)


@api.route(BASE_URL + "/user", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_user():
    """DELETE /api/v1/user?id=guid - delete user by guid"""
    guid = request.args.get("id")
    return UserController.delete(guid=guid)


@api.route(BASE_URL + "/login", methods=["POST"])
def login():
    """POST /api/v1/login - login user"""
    data = request.get_json()
    return UserController.login(data=data)


# SERVICE ROUTES


@api.route(BASE_URL + "/service", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_service():
    """POST /api/v1/service - create service"""
    data = request.get_json()
    return ServiceController.post(data=data)


@api.route(BASE_URL + "/services", methods=["GET"])
@jwt_required()
def get_services():
    """GET /api/v1/services - query all services"""
    return ServiceController.get()


@api.route(BASE_URL + "/service", methods=["GET"])
@jwt_required()
def get_service():
    """GET /api/v1/service?id=guid - query service by guid"""
    guid = request.args.get("id")
    return ServiceController.get(guid=guid)


@api.route(BASE_URL + "/service", methods=["PUT"])
@jwt_required()
@role_required("admin")
def update_service():
    """PUT /api/v1/service?id=guid - update service by guid"""
    guid = request.args.get("id")
    data = request.get_json()
    return ServiceController.put(guid=guid, data=data)


@api.route(BASE_URL + "/service", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_service():
    """DELETE /api/v1/service?id=guid - delete service by guid"""
    guid = request.args.get("id")
    return ServiceController.delete(guid=guid)


@api.route(BASE_URL + "/searchService", methods=["GET"])
@jwt_required()
def search_service():
    """GET /api/v1/searchService?name=name - query service by name"""

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


@api.route(BASE_URL + "/servicesDown", methods=["GET"])
@jwt_required()
def unavailable_services():
    """GET /api/v1/servicesDown - query all unavailable services"""

    return ServiceController.get_unavailable_services()


# LOGS ROUTES


@api.route(BASE_URL + "/logs", methods=["GET"])
@jwt_required()
def get_logs():
    """GET /api/v1/logs - query all logs"""
    sort = request.args.get("sort")
    page = request.args.get("page")
    date = request.args.get("date")
    return UserController.get_logs(sort=sort, page=page, date=date)


@api.route(BASE_URL + "/serviceLogs", methods=["GET"])
@jwt_required()
def get_service_logs():
    """GET /api/v1/serviceLogs?id=guid - query service logs by guid"""
    guid = request.args.get("id")
    sort = request.args.get("sort")
    return ServiceController.get_service_logs(guid=guid, sort=sort)
