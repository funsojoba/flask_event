from flask import Blueprint, request, jsonify
from src.services.user import me, login_user, create_user
from src.utils.response_utils import success_response, error_response

from flask_jwt_extended import jwt_required, get_jwt_identity

from src.services.ticket import get_user_tickets

user_bp = Blueprint("users", __name__)


@user_bp.route("/me/<user_id>", methods=["GET"])
def get_me(user_id):
    return jsonify(me(user_id))


@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    result = create_user(data)
    
    if "error" in result:
        return error_response("Invalid input", errors=result["errors"], status_code=400)

    return success_response(result, "User created", 201)


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result = login_user(data=data)
    
    if result.get("error"):
        return error_response("Invalid input", errors=result["errors"], status_code=400)

    return success_response(result, "Login successful", 200)


@user_bp.route("/tickets", methods=['GET'])
@jwt_required()
def user_tickets():
    user_id = get_jwt_identity()
    tickets = get_user_tickets(user_id)
    return success_response(tickets)
    