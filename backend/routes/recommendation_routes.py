import logging
from flask import Blueprint, jsonify
from backend.database.db import get_db
from backend.routes.profile_routes import get_current_user_id
from backend.ai.recommendation import generate_recommendations

logger = logging.getLogger("learning_path.recommendation_routes")
recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route("/api/recommendations", methods=["GET"])
def get_recommendations():
    user_id = get_current_user_id()
    db = next(get_db())
    try:
        recs = generate_recommendations(db, user_id)
        return jsonify(recs), 200
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        return jsonify({"error": "Failed to fetch recommendations"}), 500
    finally:
        db.close()
