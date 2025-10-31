from flask import Blueprint, jsonify, request
from modules.exercises import query

exercises_bp = Blueprint("exercises", __name__, url_prefix="/exercises")


@exercises_bp.get("/<int:exercise_id>")
def get_exercises(exercise_id: int):
    res = query.get_exersise(exercise_id)
    return jsonify(res)


@exercises_bp.patch("/<int:exercise_id>")
def update_exercises(exercise_id: int):
    title = request.json.pop("title") if "title" in request.json else None

    data = None
    if request.json:
        data = request.json

    res = query.update_exersise(exercise_id, title, data)
    return jsonify(res)


@exercises_bp.get("/types")
def get_exercises_types():
    res = query.get_exercises_types()
    return jsonify(res)


@exercises_bp.post("/media/audio")
def save_audio():
    return jsonify(request.json)


@exercises_bp.get("/media/audio")
def get_audio():
    return jsonify(request.json)
