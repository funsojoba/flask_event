from marshmallow import Schema, fields, validate, ValidationError, validates_schema



class ReserveTicketSerializer(Schema):
    event_id = fields.String(required=True)
    

class TicketSerializer(Schema):
    id = fields.String(dump_only=True)
    event_id = fields.String(required=True)
    user_id = fields.String(dump_only=True)
    status = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    