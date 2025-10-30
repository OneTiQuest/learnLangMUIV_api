from flask import Blueprint, jsonify, request
from modules.exercises import query

exercises_bp = Blueprint("exercises", __name__, url_prefix="/exercises")


@exercises_bp.get("/<int:exercise_id>")
def get_exercises(exercise_id: int):
    res = query.get_exersise(exercise_id)
    return jsonify(res)


@exercises_bp.patch("/<int:exercise_id>")
def get_exercises(exercise_id: int):
    title = request.json.get("title")
    data = request.json.get("data")
    res = query.update_exersise(exercise_id, title, data)
    return jsonify(res)


@exercises_bp.get("/types")
def get_exercises_types():
    res = query.get_exercises_types()
    return jsonify(res)

@exercises_bp.post("/media")
def save_media():
    return jsonify(request.json)
