from flask import Flask

from app.routes import route
from app.config import config, init_config

def create_flask_app():
    app = Flask(__name__)
    init_config()

    app.config["JWT_SECRET_KEY"] = config["AUTH"].get("JWT_SECRET_KEY")

    route(app)

    api_conf = config["API"]
    app.run(host=str(api_conf.get("HOST")), port=int(api_conf.get("PORT")), debug=bool(api_conf.get("DEBUG")))
    
