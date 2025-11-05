from flask import Blueprint, jsonify, request
from modules.themes import query

themes_bp = Blueprint("themes", __name__, url_prefix="/themes")


@themes_bp.get("/<int:theme_id>")
def get_theme(theme_id: int):
    res = query.get_theme(theme_id)
    return jsonify(res)


@themes_bp.patch("/<int:theme_id>")
def update_theme(theme_id: int):
    name = request.json.get("name")
    query.update_theme(theme_id, name)
    return jsonify({"success": True})


@themes_bp.delete("/<int:theme_id>")
def delete_theme(theme_id: int):
    query.delete_theme(theme_id)
    return jsonify({"success": True})


@themes_bp.get("/<int:theme_id>/exercises")
def get_exercises(theme_id: int):
    res = query.get_exercises(theme_id)
    return jsonify(res)


@themes_bp.post("/<int:theme_id>/exercises")
def create_exercises(theme_id: int):
    type_id = request.json.get("type_id")
    title = request.json.get("title")
    res = query.create_exersise(theme_id, type_id, title)
    return jsonify(res)


@themes_bp.get("/<int:theme_id>/exercises/<int:exercise_id>/next")
def get_next_exercise(theme_id: int, exercise_id: int):
    res = query.get_next_exercise(theme_id, exercise_id)
    return jsonify(res)


@themes_bp.get("/<int:theme_id>/exercises/first")
def get_exercise_first(theme_id: int):
    res = query.get_next_exercise(theme_id)
    return jsonify(res)
