from flask import Blueprint, jsonify

_bp = Blueprint('', __name__)

@_bp.get('/')
def hello_world():
    return jsonify({
        "success": True
    })