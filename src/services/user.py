from src.utils.db_utils import db

from src.models.user import User
from src.serializers.user_serializer import CreateUserSchema, LoginUserSchema
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity



def me(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}
    return {"id": user.id, "name": user.name, "email": user.email}
    
    
    

def create_user(data):
    schema = CreateUserSchema()
    
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return {"error": True, "errors": err.messages}
    
    email = validated_data.get("email")
    password = validated_data.get("password")
    name = validated_data.get("name")
    
    if User.query.filter_by(email=email).first():
        return {"error": True, "errors": "Invalid credentials"}

    hashed_pw = generate_password_hash(password)
    user = User(name=name, email=email, password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return {"message": "User created", "id": user.id}



def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted"}


def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return {"message": "User updated"}


def login_user(data):
    schema = LoginUserSchema()
    
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return {"error": True, "errors": err.messages}
    
    email = data.get("email")
    password = data.get("password")
    
    user = User.query.filter_by(email=email).first()
    
    hashed_pwd = generate_password_hash(password=password)
    
    if not user or not check_password_hash(user.password_hash, password=password):
        return {"error": True, "errors": "Invalid credentials"}
    
    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}
