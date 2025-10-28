from flask import Flask

from app.routes import route
from app.config import config, init_config

def create_flask_app():
    app = Flask(__name__)

    init_config()
    api_conf = config["API"]

    route(app)

    app.run(host=str(api_conf.get("HOST")), port=int(api_conf.get("PORT")), debug=bool(api_conf.get("DEBUG")))
    
