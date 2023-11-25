import jwt
import configs


def decode_token(token):
    try:
        payload = jwt.decode(token, configs.secret_key, algorithms=["HS256"])
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        return {"error_message": "tolong login dari awal lagi"}, 400
    except jwt.exceptions.InvalidTokenError:
        return {"error_message": "Token yang anda berikan tidak valid"}, 400
