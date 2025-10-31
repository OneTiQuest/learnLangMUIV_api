from flask import Blueprint, jsonify
from modules.roles import query

roles_bp = Blueprint('roles', __name__, url_prefix="/roles")

@roles_bp.get('/')
def roles():
    res = query.get_roles()
    return jsonify(res)
