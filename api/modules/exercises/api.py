from flask import Blueprint, jsonify, request
from modules.exercises import query
from flask_jwt_extended import jwt_required

exercises_bp = Blueprint("exercises", __name__, url_prefix="/exercises")


@exercises_bp.get("/<int:exercise_id>")
@jwt_required()
def get_exercises(exercise_id: int):
    res = query.get_exersise(exercise_id)
    return jsonify(res)


@exercises_bp.delete("/<int:exercise_id>")
@jwt_required()
def delete_exercises(exercise_id: int):
    res = query.delete_exersise(exercise_id)
    return jsonify(res)


@exercises_bp.patch("/<int:exercise_id>")
@jwt_required()
def update_exercises(exercise_id: int):
    title = request.json.pop("title") if "title" in request.json else None
    type_id = request.json.pop("type_id") if "type_id" in request.json else None

    data = None
    if request.json:
        data = request.json

    res = query.update_exersise(exercise_id, title, data, type_id)
    return jsonify(res)


@exercises_bp.get("/types")
@jwt_required()
def get_exercises_types():
    res = query.get_exercises_types()
    return jsonify(res)
