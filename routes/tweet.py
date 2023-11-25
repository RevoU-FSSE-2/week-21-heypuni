from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from datetime import datetime
from utils import decode_token
from config import db
from models.user import User
from models.tweet import Tweet
from schemas.tweet import TweetSchema

tweet_bp = Blueprint("tweet", __name__)


@tweet_bp.route("/tweet", methods=["POST"])
def post_tweet():
    data = request.json
    schema = TweetSchema()
    try:
        tweet = schema.load(data)
    except ValidationError as e:
        return jsonify({"error_message": "Validation error: " + str(e)}), 400
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error_message": "Anda harus menggunakan token authorization untuk api ini"}), 400
    payload = decode_token(token)
    user = User.query.filter_by(id=payload["user_id"]).first()
    if not user:
        return jsonify({"error_message": "User does not exist"}), 400
    if len(tweet["tweet"]) > Tweet.tweet.property.columns[0].type.length:
        return (
            jsonify({"error_message": "tweet tidak boleh lebih dari 150 karakter"}),
            400,
        )
    tweet = Tweet(user_id=user.id, published_at=datetime.utcnow(), tweet=tweet["tweet"])
    db.session.add(tweet)
    db.session.commit()
    response = {
        "tweet_id": tweet.id,
        "published_at": tweet.published_at,
        "tweet": tweet.tweet,
    }
    return jsonify(response), 200
