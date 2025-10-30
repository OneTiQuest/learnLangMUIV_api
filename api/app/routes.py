from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.config import black_list_jwt

from modules.users.api import users_bp
from modules.auth.api import auth_bp
from modules.courses.api import courses_bp
from modules.modules.api import modules_bp
from modules.langs.api import langs_bp
from modules.themes.api import themes_bp


def route(app: Flask):
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        return jti in black_list_jwt

    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(langs_bp)
    app.register_blueprint(themes_bp)

    @app.errorhandler(Exception)
    def error(error):
        err_msg = {"error": True}

        if hasattr(error, "code"):
            err_msg["code"] = error.code

        if hasattr(error, "description"):
            err_msg["description"] = error.description

        if hasattr(error, "args"):
            err_msg["args"] = error.args

        return jsonify(err_msg)
