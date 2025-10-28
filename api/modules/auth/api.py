from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.get('/auth')
def get_auth():
    return jsonify({
        "success": True
    })

@auth_bp.post('/auth')
def post_auth():
    return jsonify({
        "success": True
    })