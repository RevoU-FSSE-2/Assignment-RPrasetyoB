from flask import Blueprint, request
from app.user.models import User
from app.tweet.models import Tweet
from app.common.constants import UserRoleEnum
from db import db
import jwt
from marshmallow import Schema
import os

moderation_bp = Blueprint("moderation", __name__)

class ModerationSchema(Schema):
    pass

@moderation_bp.route("/tweet", methods=["POST"])
def toggle_tweet_spam_status():
    getToken = request.headers.get('Authorization')
    token = getToken.split()[1]

    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error_message":"Token telah kadaluarsa"}, 401
    except jwt.InvalidTokenError:
        return {"error_message":"Token tidak valid"}, 401

    user_id = payload.get("user_id")
    user = User.query.get(user_id)

    if not user or user.role != UserRoleEnum.MODERATOR.value:
        return {"error_message":"User tidak dapat melakukan aksi ini"}, 403

    data = request.get_json()
    tweet_id = data.get("tweet_id")
    is_spam = data.get("is_spam")

    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        return {"error_message": "Tweet tidak ditemukan"}, 404

    tweet.is_spam = is_spam
    db.session.commit()

    return {
        "tweet_id": tweet.id,
        "is_spam": tweet.is_spam
    }, 200


@moderation_bp.route("/user", methods=["POST"])
def suspend_user():
    getToken = request.headers.get('Authorization')
    token = getToken.split()[1]

    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error_message": "Token telah kadaluarsa"}, 401
    except jwt.InvalidTokenError:
        return {"error_message": "Token tidak valid"}, 401

    moderator_id = payload.get("user_id")
    moderator = User.query.get(moderator_id)

    if not moderator or moderator.role != UserRoleEnum.MODERATOR.value:
        return {"error_message": "User tidak dapat melakukan aksi ini"}, 403

    data = request.get_json()
    target_user_id = data.get("user_id")
    is_suspended = data.get("is_suspended")

    target_user = User.query.get(target_user_id)

    if not target_user:
        return {"error_message": "User tidak ditemukan"}, 404

    target_user.is_suspended = is_suspended
    db.session.commit()

    return {
        "user_id": target_user.id,
        "is_suspended": target_user.is_suspended
    }, 200
