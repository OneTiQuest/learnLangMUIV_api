from flask import Blueprint, jsonify
from modules.roles import query
from flask_jwt_extended import jwt_required

roles_bp = Blueprint("roles", __name__, url_prefix="/roles")


@roles_bp.get("/")
@jwt_required()
def roles():
    res = query.get_roles()
    return jsonify(res)
