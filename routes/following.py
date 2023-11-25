from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from configs import db
from models.user import User
from schemas.following import UserFollowing
from utils import decode_token


following_bp = Blueprint("following", __name__)


@following_bp.route("/following", methods=["POST"])
def follow_user():
    data = request.json
    schema = UserFollowing()
    try:
        following = schema.load(data)
    except ValidationError as e:
        return jsonify({"error_message": "Validation error: " + str(e)}), 400
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error_message": "Anda harus menggunakan token authorization untuk api ini"}), 400
    payload = decode_token(token)
    user = User.query.filter_by(id=payload["user_id"]).first()
    if not user:
        return jsonify({"error_message": "user tidak ditemukan"}), 400
    following_user = User.query.filter_by(id=following["user_id"]).first()
    if not following_user:
        return jsonify({"error_message": "user tidak ditemukan"}), 400
    if user.id == following_user.id:
        return jsonify({"error_message": "tidak bisa follow diri sendiri"}), 400
    # create condition if user found and already followed, remove from following, else add to following
    response = {}
    if user.following is None:
        user.following = []
    if following_user.id in user.following:
        response["following_status"] = "unfollow"
        user.following.remove(following_user.id)
    else:
        response["following_status"] = "follow"
        user.following.append(following_user.id)
    db.session.commit()
    return jsonify(response), 200
