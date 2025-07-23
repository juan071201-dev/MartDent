from flask import Flask
from .routes import main
from .auth import auth
from models.database import crear_base_datos

def create_app():
    app = Flask(__name__)
    app.secret_key = "clave-super-secreta"

    app.register_blueprint(main)
    app.register_blueprint(auth)

    crear_base_datos()

    return app
