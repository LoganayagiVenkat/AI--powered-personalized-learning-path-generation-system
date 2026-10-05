import logging
from flask import Blueprint, jsonify
from backend.database.db import get_db
from backend.routes.profile_routes import get_current_user_id
from backend.ai.skill_gap import analyze_student_skill_gaps

logger = logging.getLogger("learning_path.skill_gap_routes")
skill_gap_bp = Blueprint("skill_gap", __name__)

@skill_gap_bp.route("/api/skill-gap", methods=["GET"])
def get_skill_gaps():
    user_id = get_current_user_id()
    db = next(get_db())
    try:
        analysis = analyze_student_skill_gaps(db, user_id)
        return jsonify(analysis), 200
    except Exception as e:
        logger.error(f"Error analyzing skill gaps: {e}")
        return jsonify({"error": "Failed to analyze skill gaps"}), 500
    finally:
        db.close()
