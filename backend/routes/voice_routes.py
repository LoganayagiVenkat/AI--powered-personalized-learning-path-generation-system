import base64
import logging
from flask import Blueprint, request, jsonify
from backend.database.db import get_db
from backend.models.models import VoiceInteraction
from backend.routes.profile_routes import get_current_user_id
from backend.voice.speech_to_text import transcribe_audio_bytes
from backend.voice.text_to_speech import synthesize_text_to_speech
from backend.ai.chatbot import generate_chatbot_response

logger = logging.getLogger("learning_path.voice_routes")
voice_bp = Blueprint("voice", __name__)

@voice_bp.route("/api/voice-to-text", methods=["POST"])
def voice_to_text():
    """
    Receives voice audio from frontend (either file upload or base64 or fallback transcript),
    transcribes it, processes through AI Chatbot, synthesizes voice response, and returns complete packet.
    """
    user_id = get_current_user_id()
    transcribed_text = ""
    auto_respond = True

    # 1. Check if audio file was uploaded in multipart/form-data
    if "audio" in request.files:
        audio_file = request.files["audio"]
        audio_bytes = audio_file.read()
        res = transcribe_audio_bytes(audio_bytes)
        if res.get("success"):
            transcribed_text = res.get("text")
        else:
            # If Google Speech Recognition was unreachable, check if fallback transcript was provided
            transcribed_text = request.form.get("fallback_text", "")
            if not transcribed_text:
                return jsonify({"error": res.get("error", "Transcription failed")}), 400

    # 2. Check if JSON payload was provided
    elif request.is_json:
        data = request.get_json() or {}
        if "audio_base64" in data and data["audio_base64"]:
            b64_str = data["audio_base64"]
            if "," in b64_str:
                b64_str = b64_str.split(",")[1]
            try:
                audio_bytes = base64.b64decode(b64_str)
                res = transcribe_audio_bytes(audio_bytes)
                if res.get("success"):
                    transcribed_text = res.get("text")
                else:
                    transcribed_text = data.get("fallback_text", "")
            except Exception as e:
                logger.error(f"Error decoding base64 audio: {e}")
                transcribed_text = data.get("fallback_text", "")
        else:
            transcribed_text = data.get("text", "")
            auto_respond = data.get("auto_respond", True)

    if not transcribed_text:
        return jsonify({"error": "No audible speech or transcript received. Please try speaking again."}), 400

    db = next(get_db())
    try:
        # If auto_respond is enabled, run NLP Chatbot
        ai_reply = ""
        audio_response_url = None
        if auto_respond:
            chat_res = generate_chatbot_response(db, user_id, transcribed_text)
            ai_reply = chat_res.get("reply", "")

            # Synthesize voice response
            tts_res = synthesize_text_to_speech(ai_reply)
            if tts_res.get("success"):
                audio_response_url = tts_res.get("audio_url")

        # Save interaction
        db.add(VoiceInteraction(
            user_id=user_id,
            transcribed_text=transcribed_text,
            confidence=0.95,
            ai_response_text=ai_reply,
            audio_duration_seconds=3.5
        ))
        db.commit()

        return jsonify({
            "transcribed_text": transcribed_text,
            "ai_response_text": ai_reply,
            "audio_url": audio_response_url,
            "has_voice": bool(audio_response_url)
        }), 200

    except Exception as e:
        db.rollback()
        logger.error(f"Error in voice pipeline: {e}")
        return jsonify({"error": "Voice pipeline error"}), 500
    finally:
        db.close()

@voice_bp.route("/api/text-to-speech", methods=["POST"])
def text_to_speech_endpoint():
    data = request.get_json() or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text is required"}), 400

    tts_res = synthesize_text_to_speech(text)
    return jsonify(tts_res), 200
