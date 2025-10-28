from flask import Blueprint, jsonify, request
from modules.users import query

users_bp = Blueprint('users', __name__, url_prefix="/users")

# /users/
@users_bp.get('/')
def get_users():
    res = query.get_users()
    return jsonify(res)

# /users/
@users_bp.post('/')
def save_users():
    res = query.save_user(request.json)
    return jsonify(res)


# /users/1
@users_bp.get('/<int:user_id>')
def get_user(user_id: int):
    res = query.get_user(user_id)
    return jsonify(res)

# /users/1
@users_bp.patch('/<int:user_id>')
def update_user(user_id: int):
    query.update_user(user_id, request.json.role_id)
    return jsonify({"success": True})


# /users/1/modules
@users_bp.get('/<int:user_id>/modules')
def get_user_modules(user_id: int):
    res = query.get_modules(user_id)
    return jsonify(res)

# /users/1/modules
@users_bp.post('/<int:user_id>/modules')
def create_user_modules(user_id: int, module_id: int):
    module_id = request.json.module_id
    query.create_module(user_id, module_id)
    return jsonify({"success": True})


# /users/1/langs
@users_bp.post('/<int:user_id>/langs')
def create_user_lang(user_id: int):
    lang_id = request.json.lang_id
    query.create_user_lang(user_id, lang_id)
    return jsonify({"success": True})

# /users/1/langs
@users_bp.get('/<int:user_id>/langs')
def get_user_lang(user_id: int):
    res = query.get_user_langs(user_id)
    return jsonify(res)


# /users/1/grades
@users_bp.get('/<int:user_id>/grades')
def update_user_theme(user_id: int):
    res = query.get_grades(user_id)

    # TODO: Решается авторизацией
    if request.json.is_teacher:
        res = query.get_teacher_stat(user_id)

    return jsonify(res)

# /users/1/grades
@users_bp.post('/<int:user_id>/grades')
def update_user_theme(user_id: int):
    theme_id = request.json.theme_id
    grade = request.json.grade
    query.set_user_grade(user_id, theme_id, grade)
    return jsonify({"success": True})