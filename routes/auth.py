from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from datetime import datetime, timedelta
import config
from config import db, bcrypt
from models.user import User
from schemas.user import UserRegistration
import jwt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registration", methods=["POST"])
def register_user():
    data = request.json
    schema = UserRegistration()
    try:
        user = schema.load(data)
    except ValidationError as e:
        return jsonify({"error_message": "Validation error: " + str(e)}), 400
    existing_user = User.query.filter_by(username=user["username"]).first()
    if existing_user:
        return jsonify({"error_message": "username sudah digunakan"}), 400
    password_hash = bcrypt.generate_password_hash(user["password"]).decode("utf-8")
    if len(user["bio"]) > User.bio.property.columns[0].type.length:
        return jsonify({"error_message": "bio terlalu panjang"}), 400
    user = User(username=user["username"], password=password_hash, bio=user["bio"])
    db.session.add(user)
    db.session.commit()
    response = {"user_id": user.id, "username": user.username, "bio": user.bio}
    return jsonify(response), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify({"error_message": "User does not exist"}), 400
    if not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error_message": "Invalid password"}), 400
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    token = jwt.encode(payload, config.secret_key, algorithm="HS256")

    return {"id": user.id, "username": user.username, "token": token}, 200
