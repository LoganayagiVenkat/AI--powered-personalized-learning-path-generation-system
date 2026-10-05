import logging
from flask import Blueprint, request, jsonify
from backend.database.db import get_db
from backend.models.models import ChatHistory
from backend.routes.profile_routes import get_current_user_id
from backend.ai.chatbot import generate_chatbot_response

logger = logging.getLogger("learning_path.chatbot_routes")
chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/api/chat", methods=["POST"])
def send_chat_message():
    user_id = get_current_user_id()
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    db = next(get_db())
    try:
        reply_data = generate_chatbot_response(db, user_id, message)
        return jsonify(reply_data), 200
    except Exception as e:
        logger.error(f"Error generating chatbot response: {e}")
        return jsonify({"error": "Failed to process chat query"}), 500
    finally:
        db.close()

@chatbot_bp.route("/api/chat/history", methods=["GET"])
def get_chat_history():
    user_id = get_current_user_id()
    db = next(get_db())
    try:
        chats = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp.asc()).all()
        return jsonify([{
            "id": c.id,
            "role": c.role,
            "message": c.message,
            "intent": c.intent_detected,
            "timestamp": c.timestamp.isoformat()
        } for c in chats]), 200
    finally:
        db.close()
