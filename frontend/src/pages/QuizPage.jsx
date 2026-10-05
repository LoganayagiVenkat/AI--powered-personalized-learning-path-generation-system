import React, { useState, useEffect } from 'react';
import {
  Award,
  Clock,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  ArrowRight,
  ArrowLeft,
  RotateCcw,
  BookOpen,
  Layers,
  Brain,
  Shuffle,
  Lightbulb,
  Key,
  Check,
  X,
  Zap
} from 'lucide-react';
import confetti from 'canvas-confetti';
import api from '../services/api';

export default function QuizPage({ topicId, setActiveTab, setSelectedTopicId, initialMode = 'ai-generator' }) {
  // Current active mode: 'ai-generator', 'flashcards', 'standard'
  const [activeMode, setActiveMode] = useState(initialMode);

  // Topics catalog for topic dropdown selector
  const [allTopics, setAllTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(topicId || 1);

  // -------------------------------------------------------------
  // 1. STANDARD TOPIC QUIZ STATE
  // -------------------------------------------------------------
  const [standardQuiz, setStandardQuiz] = useState(null);
  const [stdCurrentIdx, setStdCurrentIdx] = useState(0);
  const [stdSelectedAnswers, setStdSelectedAnswers] = useState({});
  const [stdLoading, setStdLoading] = useState(false);
  const [stdSubmitting, setStdSubmitting] = useState(false);
  const [stdResult, setStdResult] = useState(null);
  const [stdTimeLeft, setStdTimeLeft] = useState(600);

  // -------------------------------------------------------------
  // 2. DYNAMIC AI QUIZ GENERATOR STATE
  // -------------------------------------------------------------
  const [dynNumQuestions, setDynNumQuestions] = useState(5);
  const [dynDifficulty, setDynDifficulty] = useState('Intermediate');
  const [dynFocusType, setDynFocusType] = useState('conceptual');
  const [apiKey, setApiKey] = useState(localStorage.getItem('gemini_api_key') || '');
  const [showApiKeyInput, setShowApiKeyInput] = useState(false);
  const [isGeneratingDynQuiz, setIsGeneratingDynQuiz] = useState(false);
  const [dynQuizSession, setDynQuizSession] = useState(null);
  const [dynCurrentIdx, setDynCurrentIdx] = useState(0);
  const [dynSelectedAnswers, setDynSelectedAnswers] = useState({});
  const [dynSubmitting, setDynSubmitting] = useState(false);
  const [dynResult, setDynResult] = useState(null);
  const [dynTimeLeft, setDynTimeLeft] = useState(300);

  // -------------------------------------------------------------
  // 3. INTERACTIVE 3D REVISION FLASHCARDS STATE
  // -------------------------------------------------------------
  const [flashcards, setFlashcards] = useState([]);
  const [fcNumCards, setFcNumCards] = useState(6);
  const [isGeneratingFc, setIsGeneratingFc] = useState(false);
  const [fcCurrentIdx, setFcCurrentIdx] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [masteredCards, setMasteredCards] = useState(new Set());
  const [reviewCards, setReviewCards] = useState(new Set());
  const [fcCompleted, setFcCompleted] = useState(false);

  // Load all topics catalog once for quick topic switching
  useEffect(() => {
    const fetchTopicsCatalog = async () => {
      try {
        const topics = await api.getTopics();
        if (Array.isArray(topics) && topics.length > 0) {
          setAllTopics(topics);
          if (!topicId) {
            setSelectedTopic(topics[0].id);
          }
        }
      } catch (err) {
        console.error('Error fetching topics list:', err);
      }
    };
    fetchTopicsCatalog();
  }, []);

  // Update selected topic when prop changes
  useEffect(() => {
    if (topicId) {
      setSelectedTopic(topicId);
    }
  }, [topicId]);

  // Save API key when changed
  const handleSaveApiKey = (key) => {
    setApiKey(key);
    if (key) {
      localStorage.setItem('gemini_api_key', key);
    } else {
      localStorage.removeItem('gemini_api_key');
    }
  };

  // -------------------------------------------------------------
  // STANDARD QUIZ HANDLERS
  // -------------------------------------------------------------
  const fetchStandardQuiz = async (tId) => {
    try {
      setStdLoading(true);
      setStdResult(null);
      setStdSelectedAnswers({});
      setStdCurrentIdx(0);
      const data = await api.getTopicQuiz(tId);
      setStandardQuiz(data);
      if (data?.time_limit_minutes) {
        setStdTimeLeft(data.time_limit_minutes * 60);
      }
    } catch (err) {
      console.error('Error fetching standard quiz:', err);
    } finally {
      setStdLoading(false);
    }
  };

  useEffect(() => {
    if (activeMode === 'standard') {
      fetchStandardQuiz(selectedTopic);
    }
  }, [selectedTopic, activeMode]);

  // Standard Quiz Timer
  useEffect(() => {
    if (activeMode === 'standard' && !stdResult && stdTimeLeft > 0 && standardQuiz) {
      const timer = setInterval(() => setStdTimeLeft(prev => prev - 1), 1000);
      return () => clearInterval(timer);
    }
  }, [stdTimeLeft, stdResult, standardQuiz, activeMode]);

  const handleStdSelectOption = (questionId, option) => {
    setStdSelectedAnswers(prev => ({
      ...prev,
      [String(questionId)]: option
    }));
  };

  const handleStdSubmit = async () => {
    try {
      setStdSubmitting(true);
      const res = await api.submitQuiz(standardQuiz.quiz_id, standardQuiz.topic_id, stdSelectedAnswers);
      setStdResult(res);
      if (res.passed) {
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      }
    } catch (err) {
      alert('Standard quiz submission failed: ' + err.message);
    } finally {
      setStdSubmitting(false);
    }
  };

  // -------------------------------------------------------------
  // DYNAMIC AI QUIZ GENERATION HANDLERS
  // -------------------------------------------------------------
  const handleGenerateDynQuiz = async () => {
    try {
      setIsGeneratingDynQuiz(true);
      setDynResult(null);
      setDynSelectedAnswers({});
      setDynCurrentIdx(0);
      const res = await api.generateDynamicQuiz(selectedTopic, {
        num_questions: dynNumQuestions,
        difficulty: dynDifficulty,
        focus_type: dynFocusType,
        api_key: apiKey
      });
      setDynQuizSession(res);
      setDynTimeLeft((res.total_questions || 5) * 60); // 1 minute per question
    } catch (err) {
      alert('Failed to generate AI quiz: ' + err.message);
    } finally {
      setIsGeneratingDynQuiz(false);
    }
  };

  // Auto-generate dynamic quiz on initial load if empty
  useEffect(() => {
    if (activeMode === 'ai-generator' && !dynQuizSession && !isGeneratingDynQuiz) {
      handleGenerateDynQuiz();
    }
  }, [selectedTopic, activeMode]);

  // Dynamic Quiz Timer
  useEffect(() => {
    if (activeMode === 'ai-generator' && !dynResult && dynTimeLeft > 0 && dynQuizSession) {
      const timer = setInterval(() => setDynTimeLeft(prev => prev - 1), 1000);
      return () => clearInterval(timer);
    }
  }, [dynTimeLeft, dynResult, dynQuizSession, activeMode]);

  const handleDynSelectOption = (questionId, option) => {
    setDynSelectedAnswers(prev => ({
      ...prev,
      [String(questionId)]: option
    }));
  };

  const handleDynSubmit = async () => {
    try {
      setDynSubmitting(true);
      const res = await api.submitDynamicQuiz({
        session_id: dynQuizSession.session_id,
        topic_id: selectedTopic,
        answers: dynSelectedAnswers
      });
      setDynResult(res);
      if (res.passed) {
        confetti({ particleCount: 120, spread: 80, origin: { y: 0.6 } });
      }
    } catch (err) {
      alert('Failed to evaluate dynamic quiz: ' + err.message);
    } finally {
      setDynSubmitting(false);
    }
  };

  // -------------------------------------------------------------
  // FLASHCARDS GENERATION HANDLERS
  // -------------------------------------------------------------
  const handleGenerateFlashcards = async () => {
    try {
      setIsGeneratingFc(true);
      setFcCompleted(false);
      setFcCurrentIdx(0);
      setIsFlipped(false);
      setMasteredCards(new Set());
      setReviewCards(new Set());
      const res = await api.generateFlashcards(selectedTopic, {
        num_cards: fcNumCards,
        api_key: apiKey
      });
      setFlashcards(res.flashcards || []);
    } catch (err) {
      alert('Failed to generate flashcards: ' + err.message);
    } finally {
      setIsGeneratingFc(false);
    }
  };

  useEffect(() => {
    if (activeMode === 'flashcards' && flashcards.length === 0 && !isGeneratingFc) {
      handleGenerateFlashcards();
    }
  }, [selectedTopic, activeMode]);

  const handleCardMastered = () => {
    const currentCard = flashcards[fcCurrentIdx];
    if (currentCard) {
      setMasteredCards(prev => new Set(prev).add(currentCard.id));
      setReviewCards(prev => {
        const next = new Set(prev);
        next.delete(currentCard.id);
        return next;
      });
    }
    advanceCard();
  };

  const handleCardNeedsReview = () => {
    const currentCard = flashcards[fcCurrentIdx];
    if (currentCard) {
      setReviewCards(prev => new Set(prev).add(currentCard.id));
      setMasteredCards(prev => {
        const next = new Set(prev);
        next.delete(currentCard.id);
        return next;
      });
    }
    advanceCard();
  };

  const advanceCard = () => {
    setIsFlipped(false);
    setTimeout(() => {
      if (fcCurrentIdx < flashcards.length - 1) {
        setFcCurrentIdx(prev => prev + 1);
      } else {
        setFcCompleted(true);
        confetti({ particleCount: 80, spread: 60, origin: { y: 0.6 } });
      }
    }, 180);
  };

  const handleShuffleCards = () => {
    const shuffled = [...flashcards].sort(() => Math.random() - 0.5);
    setFlashcards(shuffled);
    setFcCurrentIdx(0);
    setIsFlipped(false);
    setFcCompleted(false);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  const currentTopicObj = allTopics.find(t => t.id === Number(selectedTopic)) || {
    id: selectedTopic,
    title: 'Curriculum Topic',
    category: 'Technology'
  };

  // -------------------------------------------------------------
  // RENDER: TOP HEADER BAR & MODE SELECTOR
  // -------------------------------------------------------------
  return (
    <div className="page-wrapper" style={{ maxWidth: '960px', margin: '0 auto' }}>
      {/* Top Banner with Topic Selector & Mode Pills */}
      <div className="card-gradient-border" style={{ marginBottom: '24px', padding: '24px 28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '18px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
              <span className="badge badge-purple">{currentTopicObj.category || 'Topic'}</span>
              <span className="badge badge-blue">AI Evaluation</span>
            </div>
            <h1 style={{ fontSize: '22px', fontWeight: 800, color: '#0F172A' }}>
              Interactive Assessment & Knowledge Engine
            </h1>
          </div>

          {/* Topic Switcher Dropdown */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <label style={{ fontSize: '13px', fontWeight: 700, color: '#64748B' }}>Topic:</label>
            <select
              value={selectedTopic}
              onChange={(e) => {
                const newId = Number(e.target.value);
                setSelectedTopic(newId);
                if (setSelectedTopicId) setSelectedTopicId(newId);
              }}
              style={{
                padding: '8px 14px',
                borderRadius: '10px',
                border: '1.5px solid #CBD5E1',
                background: 'white',
                fontWeight: 600,
                fontSize: '13px',
                color: '#0F172A',
                cursor: 'pointer'
              }}
            >
              {allTopics.map(t => (
                <option key={t.id} value={t.id}>
                  {t.title}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Three Modes Navigation Pills */}
        <div className="tab-pill-bar">
          <button
            onClick={() => setActiveMode('ai-generator')}
            className={`tab-pill-btn ${activeMode === 'ai-generator' ? 'active' : ''}`}
          >
            <Sparkles size={16} color={activeMode === 'ai-generator' ? '#6366F1' : '#64748B'} />
            <span>⚡ Dynamic AI Quiz</span>
          </button>

          <button
            onClick={() => setActiveMode('flashcards')}
            className={`tab-pill-btn ${activeMode === 'flashcards' ? 'active' : ''}`}
          >
            <Layers size={16} color={activeMode === 'flashcards' ? '#6366F1' : '#64748B'} />
            <span>🃏 Revision Flashcards</span>
          </button>

          <button
            onClick={() => setActiveMode('standard')}
            className={`tab-pill-btn ${activeMode === 'standard' ? 'active' : ''}`}
          >
            <BookOpen size={16} color={activeMode === 'standard' ? '#6366F1' : '#64748B'} />
            <span>📝 Module Mastery Quiz</span>
          </button>
        </div>

        {/* Optional Gemini API Key Drawer Toggle */}
        <div style={{ borderTop: '1px solid #E2E8F0', paddingTop: '12px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px' }}>
          <span style={{ fontSize: '12px', color: '#64748B', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Brain size={14} color="#6366F1" />
            AI Engine: <strong>{apiKey ? 'Google Gemini LLM Connected' : 'Curated Intelligent NLP Generator (Zero Config)'}</strong>
          </span>

          <button
            onClick={() => setShowApiKeyInput(!showApiKeyInput)}
            style={{
              background: 'transparent',
              border: 'none',
              fontSize: '12px',
              fontWeight: 600,
              color: '#4F46E5',
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px'
            }}
          >
            <Key size={13} />
            {showApiKeyInput ? 'Hide API Key Config' : 'Custom Gemini Key (Optional)'}
          </button>
        </div>

        {showApiKeyInput && (
          <div style={{ marginTop: '12px', padding: '12px 16px', background: '#F8FAFC', borderRadius: '12px', border: '1px dashed #CBD5E1' }}>
            <label style={{ fontSize: '12px', fontWeight: 700, color: '#334155', display: 'block', marginBottom: '6px' }}>
              Google Gemini API Key:
            </label>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input
                type="password"
                placeholder="AIzaSy..."
                value={apiKey}
                onChange={(e) => handleSaveApiKey(e.target.value)}
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  borderRadius: '8px',
                  border: '1px solid #CBD5E1',
                  fontSize: '13px'
                }}
              />
              {apiKey && (
                <button
                  onClick={() => handleSaveApiKey('')}
                  className="btn btn-secondary btn-sm"
                >
                  Clear
                </button>
              )}
            </div>
            <p style={{ fontSize: '11px', color: '#64748B', marginTop: '4px' }}>
              Note: Optional. If left blank, the system automatically uses the built-in Intelligent NLP Domain Knowledge Engine with 100% offline reliability.
            </p>
          </div>
        )}
      </div>

      {/* ========================================================= */}
      {/* MODE 1: DYNAMIC AI QUIZ GENERATOR                        */}
      {/* ========================================================= */}
      {activeMode === 'ai-generator' && (
        <div>
          {/* Controls Bar for Generating Fresh AI Quizzes */}
          <div className="card" style={{ marginBottom: '24px', padding: '20px 24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px', flexWrap: 'wrap' }}>
                <div>
                  <label style={{ fontSize: '11px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase', display: 'block', marginBottom: '4px' }}>
                    Questions
                  </label>
                  <select
                    value={dynNumQuestions}
                    onChange={(e) => setDynNumQuestions(Number(e.target.value))}
                    style={{ padding: '6px 12px', borderRadius: '8px', border: '1px solid #CBD5E1', fontSize: '13px', fontWeight: 600 }}
                  >
                    <option value={3}>3 Questions (Quick)</option>
                    <option value={5}>5 Questions (Standard)</option>
                    <option value={8}>8 Questions (In-depth)</option>
                  </select>
                </div>

                <div>
                  <label style={{ fontSize: '11px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase', display: 'block', marginBottom: '4px' }}>
                    Difficulty
                  </label>
                  <select
                    value={dynDifficulty}
                    onChange={(e) => setDynDifficulty(e.target.value)}
                    style={{ padding: '6px 12px', borderRadius: '8px', border: '1px solid #CBD5E1', fontSize: '13px', fontWeight: 600 }}
                  >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                    <option value="Expert">Expert / Interview</option>
                  </select>
                </div>

                <div>
                  <label style={{ fontSize: '11px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase', display: 'block', marginBottom: '4px' }}>
                    Focus Style
                  </label>
                  <select
                    value={dynFocusType}
                    onChange={(e) => setDynFocusType(e.target.value)}
                    style={{ padding: '6px 12px', borderRadius: '8px', border: '1px solid #CBD5E1', fontSize: '13px', fontWeight: 600 }}
                  >
                    <option value="conceptual">Conceptual & Theory</option>
                    <option value="practical">Code & Real-World Pitfalls</option>
                    <option value="scenario">Production Architecture</option>
                  </select>
                </div>
              </div>

              <button
                onClick={handleGenerateDynQuiz}
                disabled={isGeneratingDynQuiz}
                className="btn btn-primary ai-pulse-btn"
                style={{ padding: '10px 20px' }}
              >
                <Sparkles size={16} />
                <span>{isGeneratingDynQuiz ? 'Synthesizing with AI...' : 'Generate Fresh AI Quiz'}</span>
              </button>
            </div>
          </div>

          {/* Loading State */}
          {isGeneratingDynQuiz && (
            <div className="card" style={{ textAlign: 'center', padding: '48px 24px', marginBottom: '24px' }}>
              <Sparkles size={40} color="#6366F1" style={{ animation: 'spin 2s linear infinite', margin: '0 auto 16px' }} />
              <h3 style={{ fontSize: '18px', fontWeight: 800, color: '#0F172A', marginBottom: '8px' }}>
                AI Knowledge Engine is Synthesizing MCQs...
              </h3>
              <p style={{ fontSize: '14px', color: '#64748B', maxWidth: '520px', margin: '0 auto' }}>
                Analyzing key concepts of <strong>{currentTopicObj.title}</strong>, crafting plausible distractor choices, and formulating detailed explanations.
              </p>
            </div>
          )}

          {/* AI Result Card */}
          {!isGeneratingDynQuiz && dynResult && (
            <div className="card-gradient-border" style={{ textAlign: 'center', padding: '36px', marginBottom: '24px' }}>
              <div style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                background: dynResult.passed ? '#ECFDF5' : '#FEF2F2',
                color: dynResult.passed ? '#059669' : '#DC2626',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '16px'
              }}>
                {dynResult.passed ? <CheckCircle2 size={36} /> : <AlertCircle size={36} />}
              </div>

              <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#0F172A', marginBottom: '6px' }}>
                {dynResult.passed ? 'Dynamic Evaluation Mastered!' : 'AI Quiz Completed - Remediation Scheduled'}
              </h2>
              <p style={{ fontSize: '14px', color: '#64748B', marginBottom: '24px' }}>
                {currentTopicObj.title} • {dynDifficulty} Level
              </p>

              <div className="grid-3" style={{ marginBottom: '24px' }}>
                <div className="card" style={{ background: '#F8FAFC' }}>
                  <span style={{ fontSize: '12px', color: '#64748B' }}>Score</span>
                  <div style={{ fontSize: '26px', fontWeight: 800, color: '#4F46E5', marginTop: '4px' }}>
                    {dynResult.score} / {dynResult.total_questions}
                  </div>
                </div>
                <div className="card" style={{ background: '#F8FAFC' }}>
                  <span style={{ fontSize: '12px', color: '#64748B' }}>Accuracy</span>
                  <div style={{ fontSize: '26px', fontWeight: 800, color: dynResult.passed ? '#059669' : '#DC2626', marginTop: '4px' }}>
                    {dynResult.percentage}%
                  </div>
                </div>
                <div className="card" style={{ background: '#F8FAFC' }}>
                  <span style={{ fontSize: '12px', color: '#64748B' }}>Status</span>
                  <div style={{ fontSize: '16px', fontWeight: 800, color: '#7C3AED', marginTop: '8px' }}>
                    {dynResult.passed ? 'Mastery Verified' : 'Adaptive Review'}
                  </div>
                </div>
              </div>

              {dynResult.adaptive_action && (
                <div className="ai-reasoning-box" style={{ textAlign: 'left', marginBottom: '24px' }}>
                  <div className="ai-reasoning-title">
                    <Sparkles size={14} /> Adaptive Path Engine Update
                  </div>
                  <p className="ai-reasoning-text">
                    {dynResult.adaptive_action}
                  </p>
                </div>
              )}

              {/* Explanations Breakdown */}
              <div style={{ textAlign: 'left', marginBottom: '28px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: 700, marginBottom: '14px' }}>AI Answer Explanations</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  {dynResult.answers_breakdown?.map((item, idx) => (
                    <div key={idx} style={{
                      padding: '16px 20px',
                      borderRadius: '12px',
                      border: '1px solid #E2E8F0',
                      background: item.is_correct ? '#F0FDF4' : '#FEF2F2'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                        <span style={{ fontSize: '14px', fontWeight: 700, color: '#0F172A' }}>
                          Question {idx + 1}: {item.question_text}
                        </span>
                        <span style={{
                          fontSize: '11px',
                          fontWeight: 700,
                          color: item.is_correct ? '#059669' : '#DC2626',
                          background: item.is_correct ? '#DCFCE7' : '#FEE2E2',
                          padding: '3px 8px',
                          borderRadius: '9999px'
                        }}>
                          {item.is_correct ? 'Correct' : 'Needs Practice'}
                        </span>
                      </div>
                      <div style={{ fontSize: '13px', color: '#475569', marginTop: '4px' }}>
                        Your Choice: <strong>{item.selected_answer || 'No answer selected'}</strong>
                      </div>
                      {!item.is_correct && (
                        <div style={{ fontSize: '13px', color: '#059669', marginTop: '2px' }}>
                          Correct Solution: <strong>{item.correct_answer}</strong>
                        </div>
                      )}
                      {item.explanation && (
                        <div style={{ fontSize: '12px', color: '#334155', marginTop: '8px', borderTop: '1px dashed #CBD5E1', paddingTop: '6px' }}>
                          💡 <em>{item.explanation}</em>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'center', gap: '12px', flexWrap: 'wrap' }}>
                <button onClick={handleGenerateDynQuiz} className="btn btn-primary">
                  <Sparkles size={16} />
                  <span>Generate Another Fresh AI Quiz</span>
                </button>
                <button onClick={() => setActiveMode('flashcards')} className="btn btn-secondary">
                  <Layers size={16} />
                  <span>Review Flashcards for This Topic</span>
                </button>
                <button onClick={() => setActiveTab('learning-path')} className="btn btn-secondary">
                  <span>Back to Learning Path</span>
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          )}

          {/* Active Dynamic Quiz Question Taking View */}
          {!isGeneratingDynQuiz && !dynResult && dynQuizSession && (
            <div>
              {/* Progress & Timer Header */}
              <div className="card" style={{ marginBottom: '20px', padding: '18px 24px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div>
                    <span style={{ fontSize: '12px', fontWeight: 700, color: '#6366F1', textTransform: 'uppercase' }}>
                      ⚡ AI Question {dynCurrentIdx + 1} of {dynQuizSession.questions?.length}
                    </span>
                    <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#0F172A' }}>
                      {dynQuizSession.topic_title}
                    </h3>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: '#FEF2F2', padding: '6px 14px', borderRadius: '9999px', color: '#DC2626', fontWeight: 700, fontSize: '13px' }}>
                    <Clock size={16} />
                    <span>{formatTime(dynTimeLeft)}</span>
                  </div>
                </div>

                <div style={{ height: '6px', background: '#F1F5F9', borderRadius: '9999px', overflow: 'hidden' }}>
                  <div style={{
                    height: '100%',
                    width: `${((dynCurrentIdx + 1) / Math.max(dynQuizSession.questions?.length || 1, 1)) * 100}%`,
                    background: 'var(--gradient-brand)',
                    borderRadius: '9999px',
                    transition: 'width 0.3s ease'
                  }} />
                </div>
              </div>

              {/* Question Card */}
              {dynQuizSession.questions?.[dynCurrentIdx] && (
                <div className="card" style={{ padding: '32px', marginBottom: '24px' }}>
                  <h3 style={{ fontSize: '17px', fontWeight: 700, color: '#0F172A', lineHeight: 1.5, marginBottom: '24px' }}>
                    {dynQuizSession.questions[dynCurrentIdx].question_text}
                  </h3>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {dynQuizSession.questions[dynCurrentIdx].options?.map((opt, oIdx) => {
                      const qIdStr = String(dynQuizSession.questions[dynCurrentIdx].id);
                      const isSelected = dynSelectedAnswers[qIdStr] === opt;
                      const letters = ['A', 'B', 'C', 'D'];
                      return (
                        <div
                          key={oIdx}
                          onClick={() => handleDynSelectOption(qIdStr, opt)}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '14px',
                            padding: '16px 20px',
                            borderRadius: '12px',
                            border: `2px solid ${isSelected ? '#6366F1' : '#E2E8F0'}`,
                            background: isSelected ? '#EEF2FF' : 'white',
                            cursor: 'pointer',
                            transition: 'all 0.15s ease'
                          }}
                        >
                          <div style={{
                            width: '28px',
                            height: '28px',
                            borderRadius: '50%',
                            background: isSelected ? '#6366F1' : '#F1F5F9',
                            color: isSelected ? 'white' : '#64748B',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: 800,
                            fontSize: '13px'
                          }}>
                            {letters[oIdx] || oIdx + 1}
                          </div>
                          <span style={{ fontSize: '14px', fontWeight: isSelected ? 700 : 500, color: isSelected ? '#312E81' : '#1E293B', flex: 1 }}>
                            {opt}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Navigation Controls */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <button
                  onClick={() => setDynCurrentIdx(prev => Math.max(prev - 1, 0))}
                  disabled={dynCurrentIdx === 0}
                  className="btn btn-secondary"
                >
                  <ArrowLeft size={16} />
                  <span>Previous</span>
                </button>

                <div style={{ display: 'flex', gap: '8px' }}>
                  {dynQuizSession.questions?.map((_, idx) => (
                    <button
                      key={idx}
                      onClick={() => setDynCurrentIdx(idx)}
                      style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '8px',
                        border: 'none',
                        background: dynCurrentIdx === idx ? '#6366F1' : (dynSelectedAnswers[String(dynQuizSession.questions[idx].id)] ? '#C7D2FE' : '#F1F5F9'),
                        color: dynCurrentIdx === idx ? 'white' : '#475569',
                        fontWeight: 700,
                        fontSize: '12px',
                        cursor: 'pointer'
                      }}
                    >
                      {idx + 1}
                    </button>
                  ))}
                </div>

                {dynCurrentIdx < (dynQuizSession.questions?.length || 1) - 1 ? (
                  <button
                    onClick={() => setDynCurrentIdx(prev => prev + 1)}
                    className="btn btn-primary"
                  >
                    <span>Next</span>
                    <ArrowRight size={16} />
                  </button>
                ) : (
                  <button
                    onClick={handleDynSubmit}
                    disabled={dynSubmitting}
                    className="btn btn-primary"
                    style={{ background: 'var(--success)' }}
                  >
                    <CheckCircle2 size={16} />
                    <span>{dynSubmitting ? 'Evaluating...' : 'Submit AI Quiz'}</span>
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ========================================================= */}
      {/* MODE 2: INTERACTIVE 3D REVISION FLASHCARDS                */}
      {/* ========================================================= */}
      {activeMode === 'flashcards' && (
        <div>
          {/* Flashcards Config Header */}
          <div className="card" style={{ marginBottom: '24px', padding: '20px 24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <div>
                  <label style={{ fontSize: '11px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase', display: 'block', marginBottom: '4px' }}>
                    Card Deck Size
                  </label>
                  <select
                    value={fcNumCards}
                    onChange={(e) => setFcNumCards(Number(e.target.value))}
                    style={{ padding: '6px 12px', borderRadius: '8px', border: '1px solid #CBD5E1', fontSize: '13px', fontWeight: 600 }}
                  >
                    <option value={4}>4 Flashcards</option>
                    <option value={6}>6 Flashcards (Recommended)</option>
                    <option value={8}>8 Flashcards (Deep Revision)</option>
                  </select>
                </div>

                <div style={{ paddingLeft: '12px', borderLeft: '1px solid #E2E8F0' }}>
                  <span style={{ fontSize: '12px', color: '#64748B', display: 'block' }}>Deck Progress:</span>
                  <div style={{ fontSize: '14px', fontWeight: 700, color: '#0F172A', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ color: '#059669' }}>✓ {masteredCards.size} Mastered</span>
                    <span style={{ color: '#F59E0B' }}>• {reviewCards.size} In Review</span>
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <button
                  onClick={handleShuffleCards}
                  disabled={flashcards.length < 2 || isGeneratingFc}
                  className="btn btn-secondary btn-sm"
                  title="Shuffle deck cards"
                >
                  <Shuffle size={15} />
                  <span>Shuffle</span>
                </button>

                <button
                  onClick={handleGenerateFlashcards}
                  disabled={isGeneratingFc}
                  className="btn btn-primary ai-pulse-btn"
                >
                  <Sparkles size={16} />
                  <span>{isGeneratingFc ? 'Generating Deck...' : 'Generate New Flashcards'}</span>
                </button>
              </div>
            </div>
          </div>

          {/* Flashcard Loading State */}
          {isGeneratingFc && (
            <div className="card" style={{ textAlign: 'center', padding: '48px 24px' }}>
              <Layers size={40} color="#6366F1" style={{ animation: 'bounce 1.5s infinite', margin: '0 auto 16px' }} />
              <h3 style={{ fontSize: '18px', fontWeight: 800, color: '#0F172A', marginBottom: '8px' }}>
                Generating Revision Flashcards...
              </h3>
              <p style={{ fontSize: '14px', color: '#64748B' }}>
                Synthesizing high-yield interview questions, memory mnemonics, and real-world code takeaways for {currentTopicObj.title}.
              </p>
            </div>
          )}

          {/* Flashcards Deck Finished Card */}
          {!isGeneratingFc && fcCompleted && (
            <div className="card-gradient-border" style={{ textAlign: 'center', padding: '40px 24px', maxWidth: '680px', margin: '0 auto' }}>
              <div style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                background: '#ECFDF5',
                color: '#059669',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '16px'
              }}>
                <Award size={36} />
              </div>
              <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#0F172A', marginBottom: '6px' }}>
                Flashcard Deck Completed!
              </h2>
              <p style={{ fontSize: '14px', color: '#64748B', marginBottom: '24px' }}>
                You reviewed all {flashcards.length} revision flashcards for {currentTopicObj.title}.
              </p>

              <div className="grid-2" style={{ maxWidth: '420px', margin: '0 auto 28px' }}>
                <div className="card" style={{ background: '#F8FAFC' }}>
                  <span style={{ fontSize: '12px', color: '#64748B' }}>Mastered</span>
                  <div style={{ fontSize: '24px', fontWeight: 800, color: '#059669', marginTop: '4px' }}>
                    {masteredCards.size} / {flashcards.length}
                  </div>
                </div>
                <div className="card" style={{ background: '#F8FAFC' }}>
                  <span style={{ fontSize: '12px', color: '#64748B' }}>Needs Review</span>
                  <div style={{ fontSize: '24px', fontWeight: 800, color: '#F59E0B', marginTop: '4px' }}>
                    {reviewCards.size}
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'center', gap: '12px', flexWrap: 'wrap' }}>
                <button
                  onClick={() => {
                    setFcCompleted(false);
                    setFcCurrentIdx(0);
                    setIsFlipped(false);
                  }}
                  className="btn btn-secondary"
                >
                  <RotateCcw size={15} />
                  <span>Restart Deck</span>
                </button>
                <button
                  onClick={() => setActiveMode('ai-generator')}
                  className="btn btn-primary"
                >
                  <Zap size={16} />
                  <span>Test with AI Quiz Now</span>
                </button>
              </div>
            </div>
          )}

          {/* Interactive 3D Card Display */}
          {!isGeneratingFc && !fcCompleted && flashcards.length > 0 && (
            <div>
              {/* Progress counter */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', maxWidth: '680px', margin: '0 auto 12px', padding: '0 4px' }}>
                <span style={{ fontSize: '13px', fontWeight: 700, color: '#4F46E5' }}>
                  Card {fcCurrentIdx + 1} of {flashcards.length}
                </span>
                <span style={{ fontSize: '12px', color: '#64748B' }}>
                  💡 Tip: Click the card to flip between front & back
                </span>
              </div>

              {/* 3D Flip Card Container */}
              <div className="flashcard-scene" onClick={() => setIsFlipped(!isFlipped)}>
                <div className={`flashcard-card ${isFlipped ? 'flipped' : ''}`}>
                  {/* FRONT FACE */}
                  <div className="flashcard-face flashcard-front">
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                        <span className="badge badge-purple">
                          {flashcards[fcCurrentIdx]?.category || 'Core Concept'}
                        </span>
                        <span className="badge badge-blue">
                          {flashcards[fcCurrentIdx]?.difficulty || 'Intermediate'}
                        </span>
                      </div>
                      <div style={{ fontSize: '12px', fontWeight: 700, color: '#6366F1', textTransform: 'uppercase', marginBottom: '8px' }}>
                        Concept Prompt / Question
                      </div>
                      <h3 style={{ fontSize: '19px', fontWeight: 800, color: '#0F172A', lineHeight: 1.5 }}>
                        {flashcards[fcCurrentIdx]?.front}
                      </h3>
                    </div>

                    <div className="flashcard-hint">
                      <RotateCcw size={13} />
                      <span>Click anywhere to reveal explanation</span>
                    </div>
                  </div>

                  {/* BACK FACE */}
                  <div className="flashcard-face flashcard-back">
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
                        <span style={{ fontSize: '12px', fontWeight: 800, color: '#4F46E5', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <CheckCircle2 size={15} /> High-Yield Answer & Key Takeaway
                        </span>
                        <span className="badge badge-purple" style={{ fontSize: '11px' }}>
                          Answer Revealed
                        </span>
                      </div>

                      <p style={{ fontSize: '15px', color: '#1E293B', lineHeight: 1.6, marginBottom: '16px', fontWeight: 500 }}>
                        {flashcards[fcCurrentIdx]?.back}
                      </p>

                      {flashcards[fcCurrentIdx]?.pro_tip && (
                        <div style={{
                          background: 'rgba(255, 255, 255, 0.85)',
                          padding: '12px 14px',
                          borderRadius: '12px',
                          border: '1px solid #C7D2FE',
                          display: 'flex',
                          alignItems: 'flex-start',
                          gap: '8px'
                        }}>
                          <Lightbulb size={16} color="#F59E0B" style={{ flexShrink: 0, marginTop: '2px' }} />
                          <div style={{ fontSize: '12px', color: '#334155' }}>
                            <strong style={{ color: '#D97706' }}>Pro Tip / Interview Gotcha:</strong> {flashcards[fcCurrentIdx]?.pro_tip}
                          </div>
                        </div>
                      )}
                    </div>

                    <div className="flashcard-hint" style={{ color: '#4F46E5' }}>
                      <RotateCcw size={13} />
                      <span>Click to flip back to question</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Buttons: Needs Review / Flip / Mastered */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px', maxWidth: '680px', margin: '0 auto' }}>
                <button
                  onClick={handleCardNeedsReview}
                  className="btn btn-secondary"
                  style={{
                    background: '#FEF3C7',
                    borderColor: '#FDE68A',
                    color: '#B45309',
                    padding: '12px 24px',
                    fontWeight: 700
                  }}
                >
                  <X size={16} />
                  <span>Needs Review</span>
                </button>

                <button
                  onClick={() => setIsFlipped(!isFlipped)}
                  className="btn btn-secondary"
                  style={{ padding: '12px 20px' }}
                >
                  <RotateCcw size={16} />
                  <span>{isFlipped ? 'Show Front' : 'Flip Card'}</span>
                </button>

                <button
                  onClick={handleCardMastered}
                  className="btn btn-primary"
                  style={{
                    background: '#10B981',
                    borderColor: '#059669',
                    padding: '12px 28px',
                    fontWeight: 700
                  }}
                >
                  <Check size={16} />
                  <span>Got It! (Mastered)</span>
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ========================================================= */}
      {/* MODE 3: STANDARD MODULE QUIZ (PRESERVED CURRICULUM QUIZ)  */}
      {/* ========================================================= */}
      {activeMode === 'standard' && (
        <div>
          {stdLoading && (
            <div className="card" style={{ textAlign: 'center', padding: '48px 24px' }}>
              <Sparkles size={36} color="#6366F1" style={{ animation: 'spin 2s linear infinite', margin: '0 auto 14px' }} />
              <p style={{ fontWeight: 600, color: '#64748B' }}>Loading standard curriculum evaluation...</p>
            </div>
          )}

          {!stdLoading && stdResult && (
            <div className="card-gradient-border" style={{ textAlign: 'center', padding: '36px' }}>
              <div style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                background: stdResult.passed ? '#ECFDF5' : '#FEF2F2',
                color: stdResult.passed ? '#059669' : '#DC2626',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '16px'
              }}>
                {stdResult.passed ? <CheckCircle2 size={36} /> : <AlertCircle size={36} />}
              </div>

              <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#0F172A', marginBottom: '6px' }}>
                {stdResult.passed ? 'Quiz Passed! Module Mastered' : 'Quiz Completed - Review Recommended'}
              </h2>
              <p style={{ fontSize: '14px', color: '#64748B', marginBottom: '24px' }}>
                {standardQuiz?.title}
              </p>

              <div className="grid-3" style={{ marginBottom: '24px' }}>
                <div className="card" style={{ background: '#F8FAFC' }}>
                  <span style={{ fontSize: '12px', color: '#64748B' }}>Score</span>
                  <div style={{ fontSize: '26px', fontWeight: 800, color: '#4F46E5', marginTop: '4px' }}>
                    {stdResult.score} / {stdResult.total_questions}
                  </div>
                </div>
                <div className="card" style={{ background: '#F8FAFC' }}>
                  <span style={{ fontSize: '12px', color: '#64748B' }}>Percentage</span>
                  <div style={{ fontSize: '26px', fontWeight: 800, color: stdResult.passed ? '#059669' : '#DC2626', marginTop: '4px' }}>
                    {stdResult.percentage}%
                  </div>
                </div>
                <div className="card" style={{ background: '#F8FAFC' }}>
                  <span style={{ fontSize: '12px', color: '#64748B' }}>Roadmap Status</span>
                  <div style={{ fontSize: '16px', fontWeight: 800, color: '#7C3AED', marginTop: '8px' }}>
                    {stdResult.passed ? 'Advanced' : 'Remedial Review'}
                  </div>
                </div>
              </div>

              {stdResult.adaptive_action && (
                <div className="ai-reasoning-box" style={{ textAlign: 'left', marginBottom: '24px' }}>
                  <div className="ai-reasoning-title">
                    <Sparkles size={14} /> Adaptive Path Engine Update
                  </div>
                  <p className="ai-reasoning-text">
                    {stdResult.adaptive_action}
                  </p>
                </div>
              )}

              {/* Explanations */}
              <div style={{ textAlign: 'left', marginBottom: '28px' }}>
                <h3 style={{ fontSize: '15px', fontWeight: 700, marginBottom: '14px' }}>Answer Explanations</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  {stdResult.answers_breakdown?.map((item, idx) => (
                    <div key={idx} style={{
                      padding: '14px 18px',
                      borderRadius: '12px',
                      border: '1px solid #E2E8F0',
                      background: item.is_correct ? '#F0FDF4' : '#FEF2F2'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                        <span style={{ fontSize: '13px', fontWeight: 700, color: '#0F172A' }}>
                          Question {idx + 1}: {item.question_text}
                        </span>
                        <span style={{
                          fontSize: '11px',
                          fontWeight: 700,
                          color: item.is_correct ? '#059669' : '#DC2626'
                        }}>
                          {item.is_correct ? 'Correct' : 'Incorrect'}
                        </span>
                      </div>
                      <div style={{ fontSize: '12px', color: '#475569', marginTop: '4px' }}>
                        Your Answer: <strong>{item.selected_answer || 'No answer selected'}</strong>
                      </div>
                      {!item.is_correct && (
                        <div style={{ fontSize: '12px', color: '#059669', marginTop: '2px' }}>
                          Correct Answer: <strong>{item.correct_answer}</strong>
                        </div>
                      )}
                      {item.explanation && (
                        <div style={{ fontSize: '12px', color: '#334155', marginTop: '6px', fontStyle: 'italic', borderTop: '1px dashed #CBD5E1', paddingTop: '4px' }}>
                          {item.explanation}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'center', gap: '12px' }}>
                <button onClick={() => setActiveTab('learning-path')} className="btn btn-primary">
                  <span>Back to AI Learning Path</span>
                  <ArrowRight size={16} />
                </button>
                <button
                  onClick={() => {
                    setStdResult(null);
                    setStdSelectedAnswers({});
                    setStdCurrentIdx(0);
                  }}
                  className="btn btn-secondary"
                >
                  <RotateCcw size={15} />
                  <span>Retry Quiz</span>
                </button>
              </div>
            </div>
          )}

          {!stdLoading && !stdResult && standardQuiz && (
            <div>
              <div className="card" style={{ marginBottom: '24px', padding: '20px 24px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div>
                    <span style={{ fontSize: '12px', fontWeight: 700, color: '#4F46E5', textTransform: 'uppercase' }}>
                      {standardQuiz?.topic_title || 'Topic Quiz'}
                    </span>
                    <h2 style={{ fontSize: '18px', fontWeight: 800, color: '#0F172A' }}>
                      Question {stdCurrentIdx + 1} of {standardQuiz?.questions?.length}
                    </h2>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: '#FEF2F2', padding: '6px 14px', borderRadius: '9999px', color: '#DC2626', fontWeight: 700, fontSize: '13px' }}>
                    <Clock size={16} />
                    <span>{formatTime(stdTimeLeft)}</span>
                  </div>
                </div>
                <div style={{ height: '6px', background: '#F1F5F9', borderRadius: '9999px', overflow: 'hidden' }}>
                  <div style={{
                    height: '100%',
                    width: `${((stdCurrentIdx + 1) / Math.max(standardQuiz?.questions?.length || 1, 1)) * 100}%`,
                    background: 'var(--gradient-brand)',
                    borderRadius: '9999px',
                    transition: 'width 0.3s ease'
                  }} />
                </div>
              </div>

              {standardQuiz.questions?.[stdCurrentIdx] && (
                <div className="card" style={{ padding: '32px', marginBottom: '24px' }}>
                  <h3 style={{ fontSize: '17px', fontWeight: 700, color: '#0F172A', lineHeight: 1.5, marginBottom: '24px' }}>
                    {standardQuiz.questions[stdCurrentIdx].question_text}
                  </h3>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {standardQuiz.questions[stdCurrentIdx].options?.map((opt, oIdx) => {
                      const qId = standardQuiz.questions[stdCurrentIdx].id;
                      const isSelected = stdSelectedAnswers[String(qId)] === opt;
                      const letters = ['A', 'B', 'C', 'D'];
                      return (
                        <div
                          key={oIdx}
                          onClick={() => handleStdSelectOption(qId, opt)}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '14px',
                            padding: '16px 20px',
                            borderRadius: '12px',
                            border: `2px solid ${isSelected ? '#6366F1' : '#E2E8F0'}`,
                            background: isSelected ? '#EEF2FF' : 'white',
                            cursor: 'pointer'
                          }}
                        >
                          <div style={{
                            width: '28px',
                            height: '28px',
                            borderRadius: '50%',
                            background: isSelected ? '#6366F1' : '#F1F5F9',
                            color: isSelected ? 'white' : '#64748B',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: 800,
                            fontSize: '13px'
                          }}>
                            {letters[oIdx] || oIdx + 1}
                          </div>
                          <span style={{ fontSize: '14px', fontWeight: isSelected ? 700 : 500, color: isSelected ? '#312E81' : '#1E293B', flex: 1 }}>
                            {opt}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Standard Nav */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <button
                  onClick={() => setStdCurrentIdx(prev => Math.max(prev - 1, 0))}
                  disabled={stdCurrentIdx === 0}
                  className="btn btn-secondary"
                >
                  <ArrowLeft size={16} />
                  <span>Previous</span>
                </button>

                <div style={{ display: 'flex', gap: '8px' }}>
                  {standardQuiz.questions?.map((_, idx) => (
                    <button
                      key={idx}
                      onClick={() => setStdCurrentIdx(idx)}
                      style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '8px',
                        border: 'none',
                        background: stdCurrentIdx === idx ? '#6366F1' : (stdSelectedAnswers[String(standardQuiz.questions[idx].id)] ? '#C7D2FE' : '#F1F5F9'),
                        color: stdCurrentIdx === idx ? 'white' : '#475569',
                        fontWeight: 700,
                        fontSize: '12px',
                        cursor: 'pointer'
                      }}
                    >
                      {idx + 1}
                    </button>
                  ))}
                </div>

                {stdCurrentIdx < (standardQuiz.questions?.length || 1) - 1 ? (
                  <button
                    onClick={() => setStdCurrentIdx(prev => prev + 1)}
                    className="btn btn-primary"
                  >
                    <span>Next</span>
                    <ArrowRight size={16} />
                  </button>
                ) : (
                  <button
                    onClick={handleStdSubmit}
                    disabled={stdSubmitting}
                    className="btn btn-primary"
                    style={{ background: 'var(--success)' }}
                  >
                    <CheckCircle2 size={16} />
                    <span>{stdSubmitting ? 'Evaluating...' : 'Submit Evaluation'}</span>
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
