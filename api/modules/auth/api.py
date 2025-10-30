from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from modules.users.query import get_auth_user, save_user, has_login
from bcrypt import gensalt, hashpw
from datetime import timedelta, datetime, timezone
from app.config import black_list_jwt

auth_bp = Blueprint('auth', __name__)
salt = gensalt()

def send_tokens(identity: str):
    role = identity.split(":")[-1]

    expires_in = timedelta(days=2)
    access_token = create_access_token(
        identity=identity,
        expires_delta=expires_in,
        additional_claims={
            "user_role": role
        }
    )
    refresh_token = create_refresh_token(identity=identity, expires_delta=timedelta(days=30))

    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=int(datetime.now(timezone.utc).timestamp() + expires_in.total_seconds()),
    )

@auth_bp.post('/login')
def login():
    login = request.json.get("login")
    password: str = request.json.get("password")

    if not login or not password:
        return abort(401)
    
    hashed_password = hashpw(password.encode(), salt).decode()
    usr_pw = "admin" if login == "admin" else hashed_password # TODO: В рамках тестового входа
    user = get_auth_user(login, usr_pw)

    if not user:
        return abort(401)
    
    identity = f"{user[0]}:{user[3]}:{user[4]}"

    return send_tokens(identity)

@auth_bp.post('/register')
def register():
    if not "login" in request.json or  not "password" in request.json:
        return abort(400)

    if has_login(request.json.get("login")):
        return abort(409)

    user_info = {
        "first_name": request.json.get("first_name"),
        "last_name": request.json.get("last_name"),
        "login": request.json.get("login"),
        "password": hashpw(request.json.get("password").encode(), salt).decode(),
        "chat_id": request.json.get("chat_id"),
        "role_id": request.json.get("role_id", 1),
    }

    new_user = save_user(user_info)

    identity = f"{new_user[0]}:{new_user[3]}:{new_user[4]}"

    return send_tokens(identity)


"""
    Bearer <REFRESH_TOKEN>
"""
@auth_bp.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return send_tokens(identity)


@auth_bp.delete('/loguot')
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    black_list_jwt[jti] = True
    return jsonify(msg="JWT revoked")
