from flask import Flask, jsonify
from modules.users.api import users_bp
from modules.auth.api import auth_bp
from modules.courses.api import courses_bp
from modules.modules.api import modules_bp
from modules.langs.api import langs_bp
from modules.themes.api import themes_bp

def route(app: Flask):
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(langs_bp)
    app.register_blueprint(themes_bp)

    @app.errorhandler(Exception)
    def error(error):
        return jsonify({
            "error": error.code,
            "description": error.description
        })
    