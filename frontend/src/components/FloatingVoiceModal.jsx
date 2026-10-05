import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2, VolumeX, X, Sparkles, ArrowRight, Play, Square } from 'lucide-react';
import api from '../services/api';

export default function FloatingVoiceModal({ isOpen, onClose }) {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [audioUrl, setAudioUrl] = useState(null);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [statusText, setStatusText] = useState('Click Speak to start voice question');
  const [loading, setLoading] = useState(false);

  const recognitionRef = useRef(null);
  const audioPlayerRef = useRef(null);

  // Initialize SpeechRecognition if available in browser
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsRecording(true);
        setStatusText('Listening... Speak your question now');
      };

      recognition.onresult = (event) => {
        let currentTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          currentTranscript += event.results[i][0].transcript;
        }
        setTranscript(currentTranscript);
      };

      recognition.onerror = (event) => {
        console.warn('Speech recognition error:', event.error);
        setIsRecording(false);
        setStatusText(`Voice recognition notice: ${event.error}. You can also type or click sample queries.`);
      };

      recognition.onend = () => {
        setIsRecording(false);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const toggleRecording = () => {
    if (isRecording) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsRecording(false);
      if (transcript.trim()) {
        processVoiceQuery(transcript.trim());
      }
    } else {
      setTranscript('');
      setAiResponse('');
      setAudioUrl(null);
      if (recognitionRef.current) {
        try {
          recognitionRef.current.start();
        } catch (e) {
          console.error(e);
          setStatusText('Voice input ready. Speak now.');
        }
      } else {
        setStatusText('Browser speech recognition active in demo mode. Choose a sample query or type below.');
      }
    }
  };

  const processVoiceQuery = async (queryText) => {
    if (!queryText.trim()) return;
    setLoading(true);
    setStatusText('Python AI Backend is processing your speech & generating response...');
    try {
      // Send to Python Backend voice-to-text / chatbot endpoint
      const result = await api.voiceToText({
        text: queryText,
        auto_respond: true
      });

      setAiResponse(result.ai_response_text || result.transcribed_text);
      setStatusText('Response received! Playing voice audio...');

      if (result.audio_url) {
        setAudioUrl(result.audio_url);
        playAudio(result.audio_url);
      } else {
        // Fallback: Browser native SpeechSynthesis
        playNativeSpeech(result.ai_response_text);
      }
    } catch (err) {
      console.error('Error processing voice query:', err);
      setStatusText('Processing error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const playAudio = (url) => {
    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause();
    }
    const audio = new Audio(url);
    audioPlayerRef.current = audio;
    setIsPlayingAudio(true);
    audio.play().catch(e => {
      console.warn('Auto-play was prevented by browser policy:', e);
      setIsPlayingAudio(false);
    });
    audio.onended = () => setIsPlayingAudio(false);
  };

  const playNativeSpeech = (text) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text.replace(/[*#•`-]/g, ''));
      utterance.rate = 1.0;
      utterance.onstart = () => setIsPlayingAudio(true);
      utterance.onend = () => setIsPlayingAudio(false);
      window.speechSynthesis.speak(utterance);
    }
  };

  const stopAudio = () => {
    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause();
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsPlayingAudio(false);
  };

  const sampleQueries = [
    "What is my next topic?",
    "Why did you recommend SQL?",
    "Explain machine learning simply.",
    "What are my weakest areas?",
    "What should I learn after Python?"
  ];

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '640px' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '38px',
              height: '38px',
              borderRadius: '10px',
              background: 'var(--gradient-brand)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white'
            }}>
              <Mic size={20} />
            </div>
            <div>
              <h3 style={{ fontSize: '18px', fontWeight: 800 }}>Python Voice Assistant</h3>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Speech-to-Text & Text-to-Speech AI Pipeline</p>
            </div>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#64748B', padding: '6px' }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Central Recording Action */}
        <div style={{
          textAlign: 'center',
          padding: '28px 20px',
          background: 'var(--gradient-soft)',
          borderRadius: '16px',
          border: '1px solid #E0E7FF',
          marginBottom: '20px'
        }}>
          {/* Pulsing Mic Circle */}
          <button
            onClick={toggleRecording}
            style={{
              width: '84px',
              height: '84px',
              borderRadius: '50%',
              background: isRecording ? '#EF4444' : 'var(--gradient-accent)',
              color: 'white',
              border: 'none',
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: isRecording ? '0 0 0 12px rgba(239, 68, 68, 0.25)' : '0 10px 25px rgba(99, 102, 241, 0.4)',
              transition: 'all 0.2s ease',
              marginBottom: '14px'
            }}
          >
            {isRecording ? <Square size={32} /> : <Mic size={36} />}
          </button>

          <p style={{ fontSize: '14px', fontWeight: 700, color: isRecording ? '#DC2626' : '#4338CA', marginBottom: '6px' }}>
            {statusText}
          </p>
          <span style={{ fontSize: '12px', color: '#64748B' }}>
            {isRecording ? 'Click the red square when you finish speaking' : 'Click the microphone button to ask anything aloud'}
          </span>
        </div>

        {/* Live Transcript Box */}
        {(transcript || isRecording) && (
          <div style={{ marginBottom: '16px' }}>
            <span style={{ fontSize: '12px', fontWeight: 700, color: '#475569', textTransform: 'uppercase' }}>
              Your Speech Transcript
            </span>
            <div style={{
              background: '#FFFFFF',
              border: '1px solid #CBD5E1',
              borderRadius: '10px',
              padding: '12px 16px',
              marginTop: '6px',
              fontSize: '14px',
              color: '#0F172A',
              minHeight: '44px',
              fontStyle: transcript ? 'normal' : 'italic'
            }}>
              {transcript || 'Listening... speak now...'}
            </div>
            {!isRecording && transcript && (
              <button
                className="btn btn-primary btn-sm"
                onClick={() => processVoiceQuery(transcript)}
                disabled={loading}
                style={{ marginTop: '8px' }}
              >
                Send Question to AI
              </button>
            )}
          </div>
        )}

        {/* AI Voice Response Output */}
        {aiResponse && (
          <div className="card" style={{ background: '#FFFFFF', border: '1px solid #C7D2FE', marginBottom: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', fontWeight: 700, color: '#4F46E5' }}>
                <Sparkles size={16} />
                <span>AI Tutor Voice Response</span>
              </div>
              <div>
                {isPlayingAudio ? (
                  <button
                    onClick={stopAudio}
                    className="btn btn-sm"
                    style={{ background: '#FEE2E2', color: '#DC2626', padding: '4px 8px' }}
                  >
                    <VolumeX size={14} /> Stop Audio
                  </button>
                ) : (
                  <button
                    onClick={() => audioUrl ? playAudio(audioUrl) : playNativeSpeech(aiResponse)}
                    className="btn btn-sm"
                    style={{ background: '#EEF2FF', color: '#4F46E5', padding: '4px 8px' }}
                  >
                    <Volume2 size={14} /> Play Voice
                  </button>
                )}
              </div>
            </div>
            <div style={{ fontSize: '14px', color: '#1E293B', lineHeight: 1.6, whiteSpace: 'pre-line' }}>
              {aiResponse}
            </div>
          </div>
        )}

        {/* Sample Voice Queries */}
        <div>
          <span style={{ fontSize: '12px', fontWeight: 700, color: '#64748B', display: 'block', marginBottom: '8px' }}>
            Or click a quick spoken prompt:
          </span>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {sampleQueries.map((q, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setTranscript(q);
                  processVoiceQuery(q);
                }}
                className="btn btn-secondary btn-sm"
                style={{ fontSize: '12px', borderRadius: '9999px', background: '#F8FAFC' }}
              >
                <span>"{q}"</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
