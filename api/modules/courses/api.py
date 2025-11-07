from flask import Blueprint, jsonify, request
from modules.courses import query

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.get("/")
def courses():
    res = query.get_courses()
    return jsonify(res)


@courses_bp.post("/")
def add_course():
    name = request.json.get("name")
    res = query.add_course(name)
    return jsonify(res)


@courses_bp.delete("/<int:cource_id>")
def delete_course(cource_id: int):
    res = query.delete_course(cource_id)
    return jsonify(res)
