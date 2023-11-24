from flask import Blueprint, jsonify, request
from app.user.models import Tweet, User
from app.auth.utils import decode_jwt

user_bp = Blueprint("user", __name__)

@user_bp.route("/", methods=["GET"])
def get_user_profile():
    token = request.headers.get('Authorization')

    if not token or not token.startswith('Bearer '):
        return {"error": "Invalid token format"}, 401

    token = token.split()[1]  # Extract the token from "Token <token>"

    # Decode the JWT to get user information
    payload = decode_jwt(token)
    if not payload:
        return jsonify({"error_message": "Token tidak valid"}), 401

    user_id = payload["user_id"]

    # Get the user from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error_message": "User not found"}), 404

    # Get the user's followers and following count
    followers_count = user.followers.count()
    following_count = user.following.count()

    # Get the user's tweets
    tweets = Tweet.query.filter_by(user_id=user.id).all()

    # Format the response
    response = {
        "user_id": user.id,
        "username": user.username,
        "bio": user.bio,
        "following": following_count,
        "followers": followers_count,
        "tweets": [{"id": tweet.id, "published_at": tweet.published_at, "tweet": tweet.tweet_text} for tweet in tweets]
    }

    return jsonify(response), 200