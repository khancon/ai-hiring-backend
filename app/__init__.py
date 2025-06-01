from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes.ai_routes import ai_bp
import logging

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    logging.basicConfig(
        level=logging.INFO,  # Or DEBUG for more verbosity
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    logger = logging.getLogger(__name__)
    logger.info("Initializing AI Hiring Backend API...")

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

    @app.route("/")
    def landing_page():
        return (
            """
            <h2>Welcome to the AI Hiring Backend API!</h2>
            <p>This API offers AI-powered hiring automation features. Use the following endpoints:</p>
            <ul>
                <li><strong>GET /health</strong> - Health check for the service.</li>
                <li><strong>POST /generate-jd</strong> - Generate a job description.<br>
                    <em>Body:</em> JSON with title, seniority, skills, location
                </li>
                <li><strong>POST /screen-resume</strong> - Screen a resume against a job description.<br>
                    <em>Form fields:</em> job_description (text), resume (file upload)
                </li>
                <li><strong>POST /generate-questions</strong> - Generate screening questions for a job.<br>
                    <em>Body:</em> JSON with title, skills
                </li>
                <li><strong>POST /evaluate</strong> - Evaluate candidate answers.<br>
                    <em>Body:</em> JSON with questions, answers
                </li>
                <li><strong>POST /generate-feedback</strong> - Generate a feedback email for candidates.<br>
                    <em>Body:</em> JSON with candidate_name, job_title, outcome, tone
                </li>
            </ul>
            <p>See <strong>/health</strong> for a simple health check.<br>
            For API usage, send POST requests as described above. You can test locally or remotely!</p>
            """,
            200,
            {"Content-Type": "text/html"}
        )



    # Simple health check route
    @app.route("/health")
    def health_check():
        return {"status": "ok"}

    return app
