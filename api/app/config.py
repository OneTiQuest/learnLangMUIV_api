import configparser, os
from bcrypt import hashpw, gensalt

config = configparser.ConfigParser()
salt = gensalt()

def init_config():
    config.add_section('DB')
    config.set('DB', 'NAME', os.environ.get("POSTGRES_DB"))
    config.set('DB', 'USER', os.environ.get("POSTGRES_USER"))
    config.set('DB', 'PASSWORD', os.environ.get("POSTGRES_PASSWORD"))
    config.set('DB', 'HOST', os.environ.get("POSTGRES_HOST"))

    config.add_section('AUTH')
    config.set('AUTH', 'JWT_SECRET_KEY', os.environ.get("JWT_SECRET_KEY"))

    config.add_section('API')
    config.set('API', 'HOST', os.environ.get("API_HOST"))
    config.set('API', 'PORT', os.environ.get("API_PORT"))
    config.set('API', 'DEBUG', os.environ.get("DEBUG"))

black_list_jwt = {}


def get_hashed_password(password: str):
    if os.environ.get("DEBUG"):
        return password

    hashed_password = hashpw(password.encode(), salt).decode()
    return hashed_password
