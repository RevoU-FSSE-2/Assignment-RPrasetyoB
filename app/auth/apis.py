from flask import Blueprint, request
from app.common.bcrypt import bcrypt
from app.user.models import User
from db import db
import jwt, os
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError

auth_bp = Blueprint("auth", __name__)

class UserRegistrationSchema(Schema):
    username = fields.String(required=True, validate=lambda x: not User.query.filter_by(username=x).first(), error="Username already exists.")
    email = fields.Email(required=True)
    password = fields.String(required=True)
    bio = fields.String(required=True)
    role = fields.String(required=True)

@auth_bp.route("/registration", methods=["POST"])
def register():
    data = request.get_json()
    schema = UserRegistrationSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        if 'username' in err.messages:
            return {"success": False, "error": "username sudah digunakan"}, 400
        else:
            return {"success": False, "error": err.messages}, 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, bio=data['bio'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()

    return {
        'success': True,
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'bio': new_user.bio,
        'role': new_user.role
    }


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"error": "User atau password tidak tepat"}, 400
    
    valid_password = bcrypt.check_password_hash(user.password, password)
    if not valid_password:
        return {"error": "User atau password tidak tepat"}, 400
    
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
    
    return {
        'id': user.id,
        'username': user.username,
        'token': token
    }
