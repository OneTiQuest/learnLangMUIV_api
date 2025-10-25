from modules.my_module import hello_world_bp

def route(app):
    app.register_blueprint(hello_world_bp)