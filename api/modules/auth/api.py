from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from modules.users.query import get_auth_user, has_login, save_user, set_chat, get_user
from datetime import timedelta, datetime, timezone
from app.config import black_list_jwt, get_hashed_password


auth_bp = Blueprint("auth", __name__)


def send_tokens(identity: str):
    role = identity.split(":")[-1]

    expires_in = timedelta(days=2)
    access_token = create_access_token(
        identity=identity,
        expires_delta=expires_in,
        additional_claims={"user_role": role},
    )
    refresh_token = create_refresh_token(
        identity=identity, expires_delta=timedelta(days=30)
    )

    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=int(
            datetime.now(timezone.utc).timestamp() + expires_in.total_seconds()
        ),
    )


@auth_bp.post("/login")
def login():
    login = request.json.get("login")
    password: str = request.json.get("password")
    chat_id: str = request.json.get("chat_id")

    if not login or not password:
        return abort(401)

    user = get_auth_user(login, get_hashed_password(password))

    if not user:
        return abort(401)
    
    user_id = user[0]
    if chat_id:
        set_chat(user_id, chat_id)

    identity = f"{user_id}:{user[3]}:{user[4]}:{user[6]}"

    return send_tokens(identity)


@auth_bp.post("/register")
def register():
    if not request.json.get("login") or not request.json.get("password"):
        return abort(400)

    if has_login(request.json.get("login")):
        return abort(409)

    user_info = {
        "first_name": request.json.get("first_name"),
        "last_name": request.json.get("last_name"),
        "login": request.json.get("login"),
        "password": get_hashed_password(request.json.get("password")),
        "chat_id": request.json.get("chat_id"),
        "role_id": request.json.get("role_id", 1),
    }
    new_user = save_user(user_info)

    identity = f"{new_user[0]}:{new_user[3]}:{new_user[4]}:{new_user[6]}"

    return send_tokens(identity)


"""
    Bearer <REFRESH_TOKEN>
"""


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user_id = int(identity[0])
    user = get_user(user_id)
    new_identity = f"{user_id}:{user[3]}:{user[4]}:{user[6]}"
    return send_tokens(new_identity)


@auth_bp.delete("/loguot")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    black_list_jwt[jti] = True
    return jsonify(msg="JWT revoked")
