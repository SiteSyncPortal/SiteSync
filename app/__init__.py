from flask import Flask
from app.models import init_app
from app.routes import main  # Assuming your Blueprint is in routes.py

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize MongoDB connection
    init_app(app)

    # Register Blueprints
    app.register_blueprint(main)

    return app
