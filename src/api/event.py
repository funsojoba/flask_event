from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.services.event import create_event, list_events
from flask_jwt_extended import jwt_required
from src.utils.response_utils import success_response, error_response
from src.serializers.event_serializer import EventCreateSchema

event_bp = Blueprint("events", __name__)




@event_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    
    data = request.get_json()
    schema = EventCreateSchema()
    
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return {"error": True, "errors": err.messages}


    result = create_event(validated_data)
    
    if result.get("error"):
        return error_response(errors=result["errors"], status_code=422)
    return success_response(result, message="Event created", status_code=201)


@event_bp.route("/", methods=["GET"])
def list_all():
    return success_response(
        data=list_events(),
    )