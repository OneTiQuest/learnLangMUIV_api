from flask import Blueprint, jsonify, request
from modules.themes import query
from flask_jwt_extended import jwt_required

themes_bp = Blueprint("themes", __name__, url_prefix="/themes")


@themes_bp.get("/<int:theme_id>")
@jwt_required()
def get_theme(theme_id: int):
    res = query.get_theme(theme_id)
    return jsonify(res)


@themes_bp.patch("/<int:theme_id>")
@jwt_required()
def update_theme(theme_id: int):
    name = request.json.get("name")
    module_id = request.json.get("module_id")
    res = query.update_theme(theme_id, name, module_id)
    return jsonify(res)


@themes_bp.delete("/<int:theme_id>")
@jwt_required()
def delete_theme(theme_id: int):
    query.delete_theme(theme_id)
    return jsonify({"success": True})


@themes_bp.get("/<int:theme_id>/exercises")
@jwt_required()
def get_exercises(theme_id: int):
    res = query.get_exercises(theme_id)
    return jsonify(res)


@themes_bp.post("/<int:theme_id>/exercises")
@jwt_required()
def create_exercises(theme_id: int):
    type_id = request.json.get("type_id")
    title = request.json.get("title")
    res = query.create_exersise(theme_id, type_id, title)
    return jsonify(res)


@themes_bp.get("/<int:theme_id>/exercises/<int:exercise_id>/next")
@jwt_required()
def get_next_exercise(theme_id: int, exercise_id: int):
    res = query.get_next_exercise(theme_id, exercise_id)
    return jsonify(res)


@themes_bp.get("/<int:theme_id>/exercises/first")
@jwt_required()
def get_exercise_first(theme_id: int):
    res = query.get_next_exercise(theme_id)
    return jsonify(res)
