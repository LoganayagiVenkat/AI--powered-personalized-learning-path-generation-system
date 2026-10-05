import os
import io
import wave
import logging
import speech_recognition as sr

logger = logging.getLogger("learning_path.stt")

def transcribe_audio_bytes(audio_bytes: bytes, file_format: str = "wav") -> dict:
    """
    Transcribe audio bytes to text using SpeechRecognition with Google Speech API
    and fallback handling.
    """
    recognizer = sr.Recognizer()

    try:
        # Check if the audio is valid wav
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)
        logger.info(f"Successfully transcribed audio: {text}")
        return {
            "success": True,
            "text": text,
            "confidence": 0.95
        }
    except sr.UnknownValueError:
        return {
            "success": False,
            "text": "",
            "error": "Speech was unintelligible. Please speak clearly into the microphone."
        }
    except sr.RequestError as e:
        logger.warning(f"Google Speech Recognition service error: {e}")
        return {
            "success": False,
            "text": "",
            "error": "Speech recognition service request error."
        }
    except Exception as e:
        logger.error(f"Error processing audio in STT: {e}")
        return {
            "success": False,
            "text": "",
            "error": f"Audio format error: {str(e)}"
        }
