import configparser, os

config = configparser.ConfigParser()

def init_config():
    debug = os.environ.get("DEBUG")

    config.add_section('DB')
    config.set('DB', 'NAME', os.environ.get("POSTGRES_DB"))
    config.set('DB', 'USER', os.environ.get("POSTGRES_USER"))
    config.set('DB', 'PASSWORD', os.environ.get("POSTGRES_PASSWORD"))
    config.set('DB', 'DEBUG', debug)

    config.add_section('API')
    config.set('API', 'HOST', os.environ.get("API_HOST"))
    config.set('API', 'PORT', os.environ.get("API_PORT"))
    config.set('API', 'DEBUG', debug)
