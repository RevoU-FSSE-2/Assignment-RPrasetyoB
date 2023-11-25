from flask import Blueprint, jsonify, request
from app.common.bcrypt import bcrypt
from app.user.models import User
from db import db
import jwt, os
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError, validates_schema
from app.common.constants import UserRoleEnum


auth_bp = Blueprint("auth", __name__)

class UserRegistrationSchema(Schema):
    username = fields.String(required=True, validate=lambda x: not User.query.filter_by(username=x).first(), error="Username already exists.")
    password = fields.String(required=True)
    bio = fields.String(required=True)
    role = fields.String(default=UserRoleEnum.USER.value)

    @validates_schema
    def validate_role(self, data, **kwargs):
        role = data.get('role', UserRoleEnum.USER.value)
        if role not in [role.value for role in UserRoleEnum]:
            raise ValidationError("Hanya 'moderator' atau 'user' yang diizinkan untuk role")

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
        
    role = data.get('role', 'user')

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password, bio=data['bio'], role=role)
    db.session.add(new_user)
    db.session.commit()

    return {
        'success': True,
        'id': new_user.id,
        'username': new_user.username,
        'bio': new_user.bio
    }


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"error": "Username atau password tidak tepat"}, 400
    
    valid_password = bcrypt.check_password_hash(user.password, password)
    if not valid_password:
        return {"error": "Username atau password tidak tepat"}, 400
    
    if user.is_suspended:
        return jsonify({"error_message": "akun telah di suspend."}), 403
    
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
    
    return {
        'id': user.id,
        'username': user.username,
        'token': token
    }
