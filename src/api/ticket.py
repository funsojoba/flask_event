from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.ticket import reserve_ticket, pay_for_ticket
from src.serializers.ticket_serializer import ReserveTicketSerializer
from src.utils.response_utils import success_response, error_response

ticket_bp = Blueprint("tickets", __name__)


@ticket_bp.route("/", methods=["POST"])
@jwt_required()
def reserve():
    data = request.get_json()
    
    schema = ReserveTicketSerializer()
    
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return {"error": True, "errors": err.messages}
    
    user_id = get_jwt_identity()
    
    result, status = reserve_ticket(
        event_id=validated_data.get("event_id"),
        user_id=user_id)
    
    if status != 201:
        return error_response(
            status_code=status,
            message="Error reserving ticket",
            errors=result.get("error")
        )

    return success_response(result, message="Ticket reserved", status_code=201)



@ticket_bp.route("/<ticket_id>/pay", methods=["POST"])
@jwt_required()
def pay(ticket_id):
    result = pay_for_ticket(ticket_id)
    return jsonify(result)

@ticket_bp.route("/for-you", methods=["GET"])
@jwt_required()
def get_user_tickets():
    user_id = get_jwt_identity()