from flask import Blueprint, jsonify
from modules.themes import query

themes_bp = Blueprint("themes", __name__, url_prefix="/themes")


@themes_bp.patch("/<int:theme_id>")
def get_theme(theme_id: int):
    query.update_theme(theme_id)
    return jsonify({"success": True})


@themes_bp.delete("/<int:theme_id>")
def delete_theme(theme_id: int):
    query.delete_theme(theme_id)
    return jsonify({"success": True})
