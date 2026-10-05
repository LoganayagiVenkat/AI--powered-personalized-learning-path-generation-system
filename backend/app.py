import os
import sys
from pathlib import Path

# Ensure project root is in sys.path so 'backend.*' imports resolve cleanly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import logging
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from backend.database.db import init_db
from backend.database.seed_data import seed_database
from backend.routes.auth_routes import auth_bp
from backend.routes.profile_routes import profile_bp
from backend.routes.assessment_routes import assessment_bp
from backend.routes.learning_path_routes import learning_path_bp
from backend.routes.quiz_routes import quiz_bp
from backend.routes.progress_routes import progress_bp
from backend.routes.skill_gap_routes import skill_gap_bp
from backend.routes.recommendation_routes import recommendation_bp
from backend.routes.chatbot_routes import chatbot_bp
from backend.routes.voice_routes import voice_bp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("learning_path.main")

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize Database and Seed Core Data
    logger.info("Initializing database and ensuring seed data...")
    init_db()
    try:
        seed_database()
    except Exception as e:
        logger.warning(f"Seed note: {e}")

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(learning_path_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(skill_gap_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(voice_bp)

    @app.route("/")
    def index():
        return jsonify({
            "system": "AI-Powered Personalized Learning Path Generation System",
            "version": "1.0.0",
            "status": "online",
            "docs": "/api/health"
        })

    @app.route("/api/health")
    def health_check():
        return jsonify({
            "status": "healthy",
            "ai_engine": "TFIDF-Cosine-DAG-KMeans-RandomForest",
            "database": "MySQL / Auto-Fallback SQLite Active",
            "endpoints": [
                "/api/register",
                "/api/login",
                "/api/profile",
                "/api/assessment",
                "/api/learning-path",
                "/api/progress",
                "/api/quiz",
                "/api/skill-gap",
                "/api/recommendations",
                "/api/chat",
                "/api/voice-to-text",
                "/api/text-to-speech"
            ]
        })

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    is_dev = os.getenv("FLASK_ENV", "development").lower() == "development"
    logger.info(f"Starting Python AI Learning Path backend server on http://localhost:{port} (debug={is_dev})")
    app.run(host="0.0.0.0", port=port, debug=is_dev, use_reloader=False)
