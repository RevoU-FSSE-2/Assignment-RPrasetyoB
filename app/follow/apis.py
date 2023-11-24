# app/follow/apis.py
from flask import Blueprint, request, jsonify
from app.user.models import User
from app.auth.utils import decode_jwt
from db import db

follow_bp = Blueprint('follow', __name__)

@follow_bp.route('/<int:user_id_to_follow>', methods=['POST'])
def follow_unfollow(user_id_to_follow):
    token = request.headers.get('Authorization')

    token = token.split()[1]

    payload = decode_jwt(token)
    if not payload:
        return jsonify({"error_message": "Token tidak valid"}), 401

    current_user = User.query.get(payload["user_id"])

    if not current_user:
        return jsonify({"error_message": "User not found"}), 404

    user_to_follow = User.query.get(user_id_to_follow)

    if not user_to_follow:
        return jsonify({"error_message": "User to follow not found"}), 404

    if current_user == user_to_follow:
        return jsonify({"error_message": "Tidak bisa follow diri sendiri"}), 400

    if current_user.is_following(user_to_follow):
        
        current_user.unfollow(user_to_follow)
        db.session.commit()
        return jsonify({"following_status": "unfollow"}), 200
    else:
        current_user.follow(user_to_follow)
        db.session.commit()
        return jsonify({"following_status": "following"}), 200