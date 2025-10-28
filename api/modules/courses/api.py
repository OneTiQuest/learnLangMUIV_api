from flask import Blueprint, jsonify
from modules.courses import query

courses_bp = Blueprint('courses', __name__, url_prefix="/courses")

@courses_bp.get('/')
def courses():
    res = query.get_courses()
    return jsonify(res)