from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes.ai_routes import ai_bp

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object(Config)
    
    # Register the AI-related routes blueprint
    # This blueprint handles all AI-related routes
    # such as job description generation, resume screening, etc.
    app.register_blueprint(ai_bp)

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
