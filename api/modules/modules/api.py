from flask import Blueprint, jsonify, request
from modules.modules import query

modules_bp = Blueprint('modules', __name__, url_prefix="/modules")

# /modules/
@modules_bp.post('/')
def create_module():
    name = request.json.name
    lang_id = request.json.lang_id
    res = query.create_module(name, lang_id)
    return jsonify(res)

# /modules/1
@modules_bp.patch('/<int:module_id>')
def update_module(module_id: int):
    res = query.update_module(module_id)
    return jsonify(res)

# /modules/1
@modules_bp.delete('/<int:module_id>')
def delete_module(module_id: int):
    res = query.delete_module(module_id)
    return jsonify(res)

# /modules/1/themes
@modules_bp.get('/<int:module_id>/themes')
def get_themes(module_id: int):
    res = query.get_themes_by_module_id(module_id)
    return jsonify(res)

# /modules/1/themes
@modules_bp.post('/<int:module_id>/themes')
def create_theme(module_id: int):
    name = request.json.name
    res = query.create_theme(module_id, name)
    return jsonify(res)