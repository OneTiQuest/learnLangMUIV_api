from flask import Blueprint, jsonify, json

hello_world_bp = Blueprint('hello_world', __name__)

@hello_world_bp.get('/')
def hello_world():
    return jsonify({
        "success": True
    })