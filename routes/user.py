from flask import request, jsonify, Blueprint
from models.user import User
from models.tweet import Tweet
from utils import decode_token


user_bp = Blueprint("user", __name__)


@user_bp.route("", methods=["GET"])
def get_user():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error_message": "Token not found"}), 400
    payload = decode_token(token)
    user = User.query.filter_by(id=payload["user_id"]).first()
    if not user:
        return jsonify({"error_message": "user tidak ditemukan"}), 400
    tweets = Tweet.query.filter_by(user_id=user.id).all()
    tweets_response = []
    for tweet in tweets:
        tweets_response.append(
            {"id": tweet.id, "published_at": tweet.published_at, "tweet": tweet.tweet}
        )
    response = {
        "id": user.id,
        "username": user.username,
        "bio": user.bio,
        "tweets": tweets_response,
    }
    return jsonify(response), 200


@user_bp.route("/feeds", methods=["GET"])
def get_feeds():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    payload = decode_token(token)
    user_id = payload["user_id"]
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user tidak ditemukan"}), 404
    tweets = Tweet.query.filter(Tweet.user_id.in_(user.following)).order_by(Tweet.published_at.desc()).limit(10).all()
    responses = []
    for tweet in tweets:
        followers = User.query.filter_by(id=tweet.user_id).first()
        data = {
            "id": tweet.id,
            "user_id": followers.id,
            "username": followers.username,
            "published_at": tweet.published_at,
            "tweet": tweet.tweet,
        }
        responses.append(data)
    return jsonify(responses), 200
