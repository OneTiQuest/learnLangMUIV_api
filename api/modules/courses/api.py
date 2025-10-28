from flask import Blueprint, jsonify
from modules.courses import query

courses_bp = Blueprint('courses', __name__)

@courses_bp.get('/courses')
def courses():
    res = query.get_courses()
    return jsonify(res)