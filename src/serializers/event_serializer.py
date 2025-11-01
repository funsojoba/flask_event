from datetime import datetime, timezone
from marshmallow import Schema, fields, validate, ValidationError, validates_schema

from src.utils.date_utils import to_utc_aware


class VenueSchema(Schema):
    address = fields.String(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    
    @validates_schema
    def validate_coordinates(self, data, **kwargs):
        lat = data.get("latitude")
        lng = data.get("longitude")

        # Latitude must be between -90 and 90
        if lat is not None and not (-90 <= lat <= 90):
            raise ValidationError("Latitude must be between -90 and 90.", "latitude")

        # Longitude must be between -180 and 180
        if lng is not None and not (-180 <= lng <= 180):
            raise ValidationError("Longitude must be between -180 and 180.", "longitude")

        # Address should not be blank
        if not data.get("address") or not data["address"].strip():
            raise ValidationError("Address cannot be empty.", "address")

class EventCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=3))
    description = fields.String(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    total_tickets = fields.Integer(required=True, validate=validate.Range(min=1))
    venue = fields.Nested(VenueSchema, required=True)
    
    @validates_schema
    def validate_dates(self, data, **kwargs):

        start = to_utc_aware(data.get("start_time"))
        end = to_utc_aware(data.get("end_time"))
        now = datetime.now(timezone.utc)

        if start is None:
            raise ValidationError("start_time is required", "start_time")
        if end is None:
            raise ValidationError("end_time is required", "end_time")

        if start <= now:
            raise ValidationError("Event start time must be in the future", "start_time")
        if end <= start:
            raise ValidationError("End time must be after start time", "end_time")
    

class EventResponseSchema(Schema):
    id = fields.String()
    title = fields.String()
    description = fields.String()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    total_tickets = fields.Integer()
    tickets_sold = fields.Integer()
    venue = fields.Nested(VenueSchema, required=True)