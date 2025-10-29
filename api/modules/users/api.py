from flask import Blueprint, jsonify, request
from modules.users import query
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

users_bp = Blueprint("users", __name__, url_prefix="/users")


# /users/
@users_bp.get("/")
@jwt_required()
def get_users():
    res = query.get_users()
    return jsonify(res, role)


# /users/
@users_bp.post("/")
def save_users():
    res = query.save_user(request.json)
    return jsonify(res)


# /users/1
@users_bp.get("/<int:user_id>")
def get_user(user_id: int):
    res = query.get_user(user_id)
    return jsonify(res)


# /users/1
@users_bp.patch("/<int:user_id>")
def update_user(user_id: int):
    query.update_user(user_id, request.json.role_id)
    return jsonify({"success": True})


# /users/1/modules
@users_bp.get("/<int:user_id>/modules")
def get_user_modules(user_id: int):
    res = query.get_modules(user_id)
    return jsonify(res)


# /users/1/modules
@users_bp.post("/<int:user_id>/modules")
def create_user_modules(user_id: int, module_id: int):
    module_id = request.json.module_id
    query.create_module(user_id, module_id)
    return jsonify({"success": True})


# /users/1/langs
@users_bp.post("/<int:user_id>/langs")
def create_user_lang(user_id: int):
    lang_id = request.json.lang_id
    query.create_user_lang(user_id, lang_id)
    return jsonify({"success": True})


# /users/1/langs
@users_bp.get("/<int:user_id>/langs")
def get_user_lang(user_id: int):
    res = query.get_user_langs(user_id)
    return jsonify(res)


# /users/1/grades
@users_bp.get("/<int:user_id>/grades")
def get_grades(user_id: int):
    res = query.get_grades(user_id)
    role = get_jwt()["user_role"]
    
    is_teacher = role == 2
    
    if is_teacher:
        res = query.get_teacher_stat(user_id)

    return jsonify(res)


# /users/1/themes/1/grades
@users_bp.post("/<int:user_id>/themes/<int:theme_id>/grades")
def set_grade(user_id: int, theme_id: int):
    grade = request.json.grade
    res = query.set_user_grade(user_id, theme_id, grade)
    return jsonify(res)


# /users/1/themes/1/answers
@users_bp.get("/<int:user_id>/themes/<int:theme_id>/answers")
def get_answers(user_id: int, theme_id: int):
    res = query.get_answers(user_id, theme_id)
    return jsonify(res)


# /users/1/exercises/1/answers
@users_bp.post("/<int:user_id>/exercises/<int:exercise_id>/answers")
def create_answer(user_id: int, exercise_id: int):
    answer = request.json.answer
    res = query.create_answer(exercise_id, user_id, answer)
    return jsonify(res)
