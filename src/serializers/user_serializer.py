from marshmallow import Schema, fields, validate, ValidationError, validates_schema


class CreateUserSchema(Schema):
    email = fields.String(required=True)
    name = fields.String(required=True)
    password = fields.String(required=True)
    

class LoginUserSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
    
    
    