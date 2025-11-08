from flask import Blueprint, jsonify, request
from modules.modules import query
from flask_jwt_extended import jwt_required

modules_bp = Blueprint("modules", __name__, url_prefix="/modules")


# /modules/
@modules_bp.post("/")
@jwt_required()
def create_module():
    name = request.json.get("name")
    lang_id = request.json.get("lang_id")
    res = query.create_module(name, lang_id)
    return jsonify(res)


# /modules/
@modules_bp.get("/")
@jwt_required()
def get_modules():
    res = query.get_modules()
    return jsonify(res)


# /modules/1
@modules_bp.get("/<int:module_id>")
@jwt_required()
def get_module(module_id: int):
    res = query.get_module(module_id)
    return jsonify(res)


# /modules/1
@modules_bp.patch("/<int:module_id>")
@jwt_required()
def update_module(module_id: int):
    name = request.json.get("name")
    lang_id = request.json.get("lang_id")
    res = query.update_module(module_id, name, lang_id)
    return jsonify(res)


# /modules/1
@modules_bp.delete("/<int:module_id>")
@jwt_required()
def delete_module(module_id: int):
    res = query.delete_module(module_id)
    return jsonify(res)


# /modules/1/themes
@modules_bp.get("/<int:module_id>/themes")
@jwt_required()
def get_themes(module_id: int):
    res = query.get_themes_by_module_id(module_id)
    return jsonify(res)


# /modules/1/themes
@modules_bp.post("/<int:module_id>/themes")
@jwt_required()
def create_theme(module_id: int):
    name = request.json.get("name")
    res = query.create_theme(module_id, name)
    return jsonify(res)


# /modules/1/courses
@modules_bp.put("/<int:module_id>/courses")
@jwt_required()
def put_module_course(module_id: int):
    courses = request.json.get("courses")
    res = query.put_module_course(module_id, courses)
    return jsonify(res)
