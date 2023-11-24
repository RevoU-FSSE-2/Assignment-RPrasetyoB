# app/tweet/apis.py
from flask import Blueprint, request, jsonify
from app.user.models import User, Tweet
from app.auth.utils import decode_jwt
from db import db
from datetime import datetime

tweet_bp = Blueprint('tweet', __name__)

@tweet_bp.route('', methods=['POST'])
def create_tweet():
    # Get the token from the Authorization header
    token = request.headers.get('Authorization')

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

    # Get the tweet text from the request body
    data = request.get_json()
    tweet_text = data.get('tweet', '')

    # Validate the length of the tweet
    if len(tweet_text) > 150:
        return jsonify({"error_message": "Tweet tidak boleh lebih dari 150 karakter"}), 400

    # Create a new tweet
    new_tweet = Tweet(user_id=user_id, tweet_text=tweet_text)
    db.session.add(new_tweet)
    db.session.commit()

    # Return the response
    response_tweet = {
        "id": new_tweet.id,
        "published_at": new_tweet.published_at,
        "tweet": new_tweet.tweet_text
    }

    return jsonify(response_tweet), 200
