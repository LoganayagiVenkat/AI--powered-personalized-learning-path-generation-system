import json
import logging
from flask import Blueprint, request, jsonify
from backend.database.db import get_db
from backend.models.models import (
    User, LearningPath, LearningPathTopic, Topic, Subtopic, StudentProfile, CareerGoal
)
from backend.routes.profile_routes import get_current_user_id
from backend.ai.learning_path import generate_personalized_learning_path

logger = logging.getLogger("learning_path.routes")
learning_path_bp = Blueprint("learning_path", __name__)

@learning_path_bp.route("/api/learning-path", methods=["GET"])
def get_learning_path():
    user_id = get_current_user_id()
    db = next(get_db())
    try:
        path = db.query(LearningPath).filter(LearningPath.user_id == user_id).first()
        if not path:
            # Generate path on demand
            logger.info(f"No existing learning path for user {user_id}. Generating initial AI path...")
            generated = generate_personalized_learning_path(db, user_id)
            return jsonify(generated), 200

        lpts = db.query(LearningPathTopic).filter(
            LearningPathTopic.learning_path_id == path.id
        ).order_by(LearningPathTopic.sequence_order).all()

        topics_data = []
        for lpt in lpts:
            t = lpt.topic
            prereqs = [pr.topic.title for pr in t.subtopics] if False else []
            topics_data.append({
                "id": t.id,
                "sequence_order": lpt.sequence_order,
                "title": t.title,
                "category": t.category,
                "difficulty": t.difficulty,
                "estimated_hours": t.estimated_hours,
                "status": lpt.status,
                "score": lpt.score,
                "recommended_reason": lpt.recommended_reason,
                "is_adaptive_addition": lpt.is_adaptive_addition,
                "estimated_learning_time": lpt.estimated_learning_time,
                "resources": json.loads(t.resources_json or "[]"),
                "practice_exercises": json.loads(t.practice_exercises_json or "[]")
            })

        career = path.career_goal
        return jsonify({
            "learning_path_id": path.id,
            "title": path.title,
            "target_career": career.title if career else "Data Scientist",
            "target_role": career.target_role if career else "Data Scientist",
            "overall_progress": path.overall_progress,
            "total_topics": path.total_topics,
            "completed_topics": path.completed_topics,
            "ai_reasoning": path.ai_reasoning,
            "algorithm": path.generated_by_algorithm,
            "topics": topics_data
        }), 200
    except Exception as e:
        logger.error(f"Error fetching learning path: {e}")
        return jsonify({"error": "Failed to load learning path"}), 500
    finally:
        db.close()

@learning_path_bp.route("/api/learning-path/generate", methods=["POST"])
def trigger_generation():
    user_id = get_current_user_id()
    db = next(get_db())
    try:
        result = generate_personalized_learning_path(db, user_id)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error generating learning path: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@learning_path_bp.route("/api/topics", methods=["GET"])
def get_all_topics():
    db = next(get_db())
    try:
        topics = db.query(Topic).all()
        return jsonify([{
            "id": t.id,
            "title": t.title,
            "category": t.category,
            "difficulty": t.difficulty,
            "estimated_hours": t.estimated_hours,
            "description": t.description,
            "concepts": json.loads(t.key_concepts_json or "[]"),
            "resources": json.loads(t.resources_json or "[]"),
            "practice_exercises": json.loads(t.practice_exercises_json or "[]")
        } for t in topics]), 200
    finally:
        db.close()

@learning_path_bp.route("/api/topics/<int:topic_id>", methods=["GET"])
def get_topic_detail(topic_id: int):
    db = next(get_db())
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return jsonify({"error": "Topic not found"}), 404

        subtopics = [{
            "id": st.id,
            "title": st.title,
            "order_index": st.order_index,
            "summary": st.summary,
            "content": st.learning_content
        } for st in topic.subtopics]

        return jsonify({
            "id": topic.id,
            "title": topic.title,
            "category": topic.category,
            "difficulty": topic.difficulty,
            "estimated_hours": topic.estimated_hours,
            "description": topic.description,
            "concepts": json.loads(topic.key_concepts_json or "[]"),
            "resources": json.loads(topic.resources_json or "[]"),
            "practice_exercises": json.loads(topic.practice_exercises_json or "[]"),
            "subtopics": subtopics
        }), 200
    finally:
        db.close()
