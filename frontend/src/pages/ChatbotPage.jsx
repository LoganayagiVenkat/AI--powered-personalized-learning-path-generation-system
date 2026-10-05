import React, { useState, useEffect, useRef } from 'react';
import {
  MessageSquare,
  Send,
  Mic,
  Volume2,
  Sparkles,
  Bot,
  User,
  History,
  Trash2
} from 'lucide-react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function ChatbotPage({ onOpenVoice }) {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [playingAudioId, setPlayingAudioId] = useState(null);
  const messagesEndRef = useRef(null);
  const audioRef = useRef(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const history = await api.getChatHistory();
        if (history && history.length > 0) {
          setMessages(history);
        } else {
          // Default initial welcome message
          setMessages([
            {
              id: 0,
              role: 'assistant',
              message: `Hello ${user?.name || 'Alex'}! I am your AI Personalized Learning Tutor. I have access to your live learning roadmap, current topic, and quiz performance for your goal as a **${user?.target_job_role || 'Data Scientist'}**.\n\nAsk me anything like:\n• "What should I learn next?"\n• "Explain machine learning simply."\n• "Why did you recommend SQL?"\n• "What are my weakest areas?"`,
              timestamp: new Date().toISOString()
            }
          ]);
        }
      } catch (err) {
        console.error('Error fetching chat history:', err);
      }
    };
    fetchHistory();
  }, [user]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const text = textToSend || inputText;
    if (!text.trim() || loading) return;

    const userMsg = {
      id: Date.now(),
      role: 'student',
      message: text.trim(),
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setLoading(true);

    try {
      const res = await api.sendMessage(text.trim());
      const botMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        message: res.reply,
        intent: res.intent,
        timestamp: res.timestamp || new Date().toISOString()
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      console.error('Error sending message:', err);
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          message: 'Sorry, I encountered an issue processing your query. Please check your backend connection.',
          timestamp: new Date().toISOString()
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSpeakMessage = async (msgId, text) => {
    try {
      if (audioRef.current) {
        audioRef.current.pause();
      }
      setPlayingAudioId(msgId);
      const res = await api.textToSpeech(text);
      if (res?.audio_url) {
        const audio = new Audio(res.audio_url);
        audioRef.current = audio;
        audio.play();
        audio.onended = () => setPlayingAudioId(null);
      } else if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text.replace(/[*#•`-]/g, ''));
        utterance.onend = () => setPlayingAudioId(null);
        window.speechSynthesis.speak(utterance);
      }
    } catch (err) {
      console.error('Error playing TTS:', err);
      setPlayingAudioId(null);
    }
  };

  const promptSuggestions = [
    "What should I learn after Python?",
    "Explain machine learning simply.",
    "Why did you recommend SQL?",
    "What are my weakest areas?",
    "What is my next topic?"
  ];

  return (
    <div className="page-wrapper" style={{ height: 'calc(100vh - 100px)', display: 'flex', flexDirection: 'column' }}>
      {/* Top Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 800, color: '#0F172A', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Bot size={22} color="#6366F1" /> AI Learning Tutor & Voice Assistant
          </h2>
          <p style={{ fontSize: '13px', color: '#64748B' }}>
            Context-aware conversational intelligence connected to your roadmap database
          </p>
        </div>

        <button
          onClick={onOpenVoice}
          className="btn btn-secondary btn-sm"
          style={{ gap: '6px' }}
        >
          <Mic size={15} color="#4F46E5" />
          <span>Launch Voice Modal</span>
        </button>
      </div>

      {/* Main Chat Container */}
      <div className="card" style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden' }}>
        {/* Messages Stream */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '24px', display: 'flex', flexDirection: 'column', gap: '18px' }}>
          {messages.map((m) => {
            const isUser = m.role === 'student' || m.role === 'user';
            return (
              <div
                key={m.id}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '12px',
                  alignSelf: isUser ? 'flex-end' : 'flex-start',
                  maxWidth: '80%'
                }}
              >
                {!isUser && (
                  <div style={{
                    width: '34px',
                    height: '34px',
                    borderRadius: '10px',
                    background: 'var(--gradient-brand)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    flexShrink: 0
                  }}>
                    <Sparkles size={16} />
                  </div>
                )}

                <div style={{
                  background: isUser ? 'var(--gradient-accent)' : '#F8FAFC',
                  color: isUser ? '#FFFFFF' : '#1E293B',
                  borderRadius: isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
                  padding: '14px 18px',
                  border: isUser ? 'none' : '1px solid #E2E8F0',
                  boxShadow: isUser ? '0 4px 12px rgba(99, 102, 241, 0.25)' : 'none',
                  fontSize: '14px',
                  lineHeight: 1.6,
                  whiteSpace: 'pre-line'
                }}>
                  {m.message}

                  {/* Audio Playback button on AI messages */}
                  {!isUser && (
                    <div style={{ marginTop: '8px', display: 'flex', justifyContent: 'flex-end' }}>
                      <button
                        onClick={() => handleSpeakMessage(m.id, m.message)}
                        style={{
                          background: 'transparent',
                          border: 'none',
                          cursor: 'pointer',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px',
                          color: playingAudioId === m.id ? '#10B981' : '#64748B',
                          fontSize: '11px',
                          fontWeight: 600
                        }}
                      >
                        <Volume2 size={13} />
                        <span>{playingAudioId === m.id ? 'Playing Voice...' : 'Listen'}</span>
                      </button>
                    </div>
                  )}
                </div>

                {isUser && (
                  <div style={{
                    width: '34px',
                    height: '34px',
                    borderRadius: '10px',
                    background: '#C7D2FE',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#312E81',
                    fontWeight: 700,
                    fontSize: '13px',
                    flexShrink: 0
                  }}>
                    U
                  </div>
                )}
              </div>
            );
          })}

          {loading && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ width: '34px', height: '34px', borderRadius: '10px', background: 'var(--gradient-brand)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white' }}>
                <Sparkles size={16} />
              </div>
              <div style={{ background: '#F1F5F9', padding: '10px 18px', borderRadius: '16px', fontSize: '13px', color: '#64748B' }}>
                Tutor is synthesizing response from your roadmap data...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Prompt Suggestions */}
        <div style={{ padding: '8px 20px', background: '#F8FAFC', borderTop: '1px solid #E2E8F0', display: 'flex', gap: '8px', overflowX: 'auto' }}>
          {promptSuggestions.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(prompt)}
              style={{
                background: '#FFFFFF',
                border: '1px solid #CBD5E1',
                borderRadius: '9999px',
                padding: '6px 12px',
                fontSize: '12px',
                fontWeight: 500,
                color: '#334155',
                cursor: 'pointer',
                whiteSpace: 'nowrap'
              }}
            >
              {prompt}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div style={{ padding: '16px 20px', borderTop: '1px solid #E2E8F0', display: 'flex', alignItems: 'center', gap: '12px', background: '#FFFFFF' }}>
          <button
            onClick={onOpenVoice}
            className="btn btn-secondary"
            style={{ borderRadius: '50%', width: '42px', height: '42px', padding: 0 }}
            title="Speak with Voice"
          >
            <Mic size={18} color="#4F46E5" />
          </button>

          <input
            type="text"
            className="form-input"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSend();
            }}
            placeholder="Ask anything about your learning path, topics, quizzes, or concepts..."
            style={{ flex: 1, borderRadius: '9999px', padding: '10px 20px' }}
          />

          <button
            onClick={() => handleSend()}
            disabled={!inputText.trim() || loading}
            className="btn btn-primary"
            style={{ borderRadius: '50%', width: '42px', height: '42px', padding: 0 }}
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
