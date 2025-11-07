from flask import Blueprint, jsonify, request
from modules.langs import query

langs_bp = Blueprint("langs", __name__, url_prefix="/langs")


@langs_bp.get("/")
def langs():
    res = query.get_langs()
    return jsonify(res)


@langs_bp.post("/")
def add_lang():
    name = request.json.get("name")
    res = query.add_lang(name)
    return jsonify(res)


@langs_bp.delete("/<int:lang_id>")
def delete_lang(lang_id: int):
    res = query.delete_lang(lang_id)
    return jsonify(res)
