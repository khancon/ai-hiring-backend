from flask import Flask
from flask_cors import CORS
from app.config import Config

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object(Config)

    # Enable CORS (allow frontend to access backend)
    CORS(app)

    # (Optional) Import and register blueprints here
    # from app.routes.ai_routes import ai_bp
    # app.register_blueprint(ai_bp)

    # Simple health check route
    @app.route("/health")
    def health_check():
        return {"status": "ok"}

    return app
