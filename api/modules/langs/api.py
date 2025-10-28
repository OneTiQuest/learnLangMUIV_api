from flask import Blueprint, jsonify
from modules.langs import query

langs_bp = Blueprint('langs', __name__, url_prefix="/langs")

@langs_bp.get('/')
def langs():
    res = query.get_langs()
    return jsonify(res)