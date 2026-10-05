import os
import io
import re
import base64
import logging

logger = logging.getLogger("learning_path.tts")

def clean_for_speech(text: str) -> str:
    """Strip markdown formatting (asterisks, hashes, bullets) so TTS reads naturally."""
    if not text:
        return ""
    text = re.sub(r"\*\*|\*|\#|`", "", text)
    text = re.sub(r"•|- ", "", text)
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)
    return text.strip()

def synthesize_text_to_speech(text: str) -> dict:
    """
    Convert text to speech audio.
    Attempts gTTS (Google Text-to-Speech) first, returns base64 mp3 data URI.
    """
    clean = clean_for_speech(text)
    if not clean:
        return {"success": False, "audio_base64": None, "error": "Empty text"}

    # Limit length for rapid TTS response
    if len(clean) > 500:
        clean = clean[:500] + "..."

    # 1. Try gTTS
    try:
        from gtts import gTTS
        fp = io.BytesIO()
        tts = gTTS(text=clean, lang="en", slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_b64 = base64.b64encode(fp.read()).decode("utf-8")
        data_uri = f"data:audio/mp3;base64,{audio_b64}"
        return {
            "success": True,
            "audio_url": data_uri,
            "format": "mp3",
            "text": clean
        }
    except Exception as e:
        logger.warning(f"gTTS online synthesis error: {e}. Trying pyttsx3 fallback.")

    # 2. Try pyttsx3 offline fallback
    try:
        import pyttsx3
        import tempfile
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        engine.save_to_file(clean, tmp_path)
        engine.runAndWait()
        
        with open(tmp_path, "rb") as f:
            wav_bytes = f.read()
        os.remove(tmp_path)

        audio_b64 = base64.b64encode(wav_bytes).decode("utf-8")
        data_uri = f"data:audio/wav;base64,{audio_b64}"
        return {
            "success": True,
            "audio_url": data_uri,
            "format": "wav",
            "text": clean
        }
    except Exception as e2:
        logger.error(f"pyttsx3 synthesis error: {e2}")
        return {
            "success": False,
            "audio_url": None,
            "text": clean,
            "error": "TTS engine error. Browser native speech synthesis will handle playback."
        }
