import React, { useState, useEffect } from 'react';
import {
  ClipboardCheck,
  Clock,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  ArrowRight,
  RotateCcw
} from 'lucide-react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function SkillAssessmentPage({ setActiveTab }) {
  const { refreshProfile } = useAuth();
  const [assessment, setAssessment] = useState(null);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [timeLeft, setTimeLeft] = useState(900); // 15 minutes

  useEffect(() => {
    const fetchAssessment = async () => {
      try {
        setLoading(true);
        const data = await api.getAssessment();
        setAssessment(data);
        if (data?.time_limit_minutes) {
          setTimeLeft(data.time_limit_minutes * 60);
        }
      } catch (err) {
        console.error('Error loading assessment:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAssessment();
  }, []);

  // Timer countdown
  useEffect(() => {
    if (!result && timeLeft > 0) {
      const timer = setInterval(() => setTimeLeft(prev => prev - 1), 1000);
      return () => clearInterval(timer);
    }
  }, [timeLeft, result]);

  const handleSelectOption = (questionId, option) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [String(questionId)]: option
    }));
  };

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      const res = await api.submitAssessment(selectedAnswers);
      setResult(res.result);
      await refreshProfile();
    } catch (err) {
      console.error('Error submitting assessment:', err);
      alert('Failed to submit assessment: ' + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  if (loading) {
    return (
      <div className="page-wrapper" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <Sparkles size={36} color="#6366F1" style={{ animation: 'spin 2s linear infinite' }} />
          <p style={{ marginTop: '12px', fontWeight: 600, color: '#64748B' }}>Loading diagnostic technical assessment...</p>
        </div>
      </div>
    );
  }

  // Result Screen after submission
  if (result) {
    return (
      <div className="page-wrapper">
        <div className="card-gradient-border" style={{ maxWidth: '800px', margin: '0 auto', textAlign: 'center' }}>
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
            <CheckCircle2 size={36} />
          </div>

          <h1 style={{ fontSize: '26px', fontWeight: 800, color: '#0F172A', marginBottom: '8px' }}>
            Assessment Complete!
          </h1>
          <p style={{ fontSize: '15px', color: '#64748B', marginBottom: '24px' }}>
            Your baseline has been computed and your AI learning path has been automatically generated.
          </p>

          {/* Score & Assigned Level */}
          <div className="grid-3" style={{ marginBottom: '28px' }}>
            <div className="card" style={{ background: '#F8FAFC' }}>
              <span style={{ fontSize: '12px', color: '#64748B', fontWeight: 600 }}>Score</span>
              <div style={{ fontSize: '26px', fontWeight: 800, color: '#4F46E5', marginTop: '4px' }}>
                {result.score} / {result.total_questions}
              </div>
            </div>
            <div className="card" style={{ background: '#F8FAFC' }}>
              <span style={{ fontSize: '12px', color: '#64748B', fontWeight: 600 }}>Percentage</span>
              <div style={{ fontSize: '26px', fontWeight: 800, color: '#059669', marginTop: '4px' }}>
                {result.percentage}%
              </div>
            </div>
            <div className="card" style={{ background: '#F8FAFC' }}>
              <span style={{ fontSize: '12px', color: '#64748B', fontWeight: 600 }}>Classified Level</span>
              <div style={{ fontSize: '24px', fontWeight: 800, color: '#7C3AED', marginTop: '4px' }}>
                {result.assigned_level}
              </div>
            </div>
          </div>

          {/* Strong vs Weak Breakdown */}
          <div style={{ textAlign: 'left', marginBottom: '28px' }}>
            <div style={{ marginBottom: '16px' }}>
              <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#059669', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <CheckCircle2 size={16} /> Strong Topics
              </h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {result.strong_topics?.length > 0 ? (
                  result.strong_topics.map((t, idx) => (
                    <span key={idx} className="badge badge-green">{t}</span>
                  ))
                ) : (
                  <span style={{ fontSize: '13px', color: '#64748B' }}>Foundational review required across all subjects.</span>
                )}
              </div>
            </div>

            <div>
              <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#DC2626', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <AlertCircle size={16} /> Topics Scheduled for Priority Reinforcement
              </h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {result.weak_topics?.length > 0 ? (
                  result.weak_topics.map((t, idx) => (
                    <span key={idx} className="badge badge-amber">{t}</span>
                  ))
                ) : (
                  <span style={{ fontSize: '13px', color: '#64748B' }}>None! Excellent baseline.</span>
                )}
              </div>
            </div>
          </div>

          {/* Action to Jump to Learning Path */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: '14px' }}>
            <button
              onClick={() => setActiveTab('learning-path')}
              className="btn btn-primary btn-lg"
            >
              <span>Explore Your AI Learning Path</span>
              <ArrowRight size={18} />
            </button>
            <button
              onClick={() => {
                setResult(null);
                setSelectedAnswers({});
                setCurrentIdx(0);
              }}
              className="btn btn-secondary"
            >
              <RotateCcw size={16} />
              <span>Retake Diagnostic</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  const questions = assessment?.questions || [];
  const currentQ = questions[currentIdx];
  const progressPct = ((currentIdx + 1) / Math.max(questions.length, 1)) * 100;
  const answeredCount = Object.keys(selectedAnswers).length;

  return (
    <div className="page-wrapper" style={{ maxWidth: '840px', margin: '0 auto' }}>
      {/* Header Bar */}
      <div className="card" style={{ marginBottom: '24px', padding: '18px 24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <div>
            <span style={{ fontSize: '12px', fontWeight: 700, color: '#4F46E5', textTransform: 'uppercase' }}>
              Initial Skill Assessment
            </span>
            <h2 style={{ fontSize: '18px', fontWeight: 800, color: '#0F172A' }}>
              Question {currentIdx + 1} of {questions.length}
            </h2>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: '#FEF2F2', padding: '6px 14px', borderRadius: '9999px', color: '#DC2626', fontWeight: 700, fontSize: '13px' }}>
            <Clock size={16} />
            <span>{formatTime(timeLeft)}</span>
          </div>
        </div>

        {/* Progress bar */}
        <div style={{ height: '6px', background: '#F1F5F9', borderRadius: '9999px', overflow: 'hidden' }}>
          <div style={{ height: '100%', width: `${progressPct}%`, background: 'var(--gradient-brand)', borderRadius: '9999px', transition: 'width 0.3s ease' }} />
        </div>
      </div>

      {/* Question Card */}
      {currentQ && (
        <div className="card" style={{ padding: '32px', marginBottom: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <span className="badge badge-purple">{currentQ.topic_title}</span>
            <span className="badge badge-blue">{currentQ.difficulty}</span>
          </div>

          <h3 style={{ fontSize: '17px', fontWeight: 700, color: '#0F172A', lineHeight: 1.5, marginBottom: '24px' }}>
            {currentQ.question_text}
          </h3>

          {/* Options */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {currentQ.options.map((option, idx) => {
              const isSelected = selectedAnswers[String(currentQ.id)] === option;
              return (
                <button
                  key={idx}
                  onClick={() => handleSelectOption(currentQ.id, option)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '14px',
                    padding: '14px 18px',
                    borderRadius: '12px',
                    border: isSelected ? '2px solid #6366F1' : '1px solid #E2E8F0',
                    background: isSelected ? '#EEF2FF' : '#FFFFFF',
                    cursor: 'pointer',
                    textAlign: 'left',
                    fontFamily: 'inherit',
                    fontSize: '14px',
                    color: isSelected ? '#312E81' : '#1E293B',
                    fontWeight: isSelected ? 600 : 400,
                    transition: 'all 0.15s ease'
                  }}
                >
                  <div style={{
                    width: '24px',
                    height: '24px',
                    borderRadius: '50%',
                    border: isSelected ? '6px solid #6366F1' : '2px solid #CBD5E1',
                    background: 'white',
                    flexShrink: 0
                  }} />
                  <span>{option}</span>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Navigation Buttons */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <button
          onClick={() => setCurrentIdx(prev => Math.max(0, prev - 1))}
          disabled={currentIdx === 0}
          className="btn btn-secondary"
        >
          Previous
        </button>

        <span style={{ fontSize: '13px', color: '#64748B' }}>
          {answeredCount} of {questions.length} answered
        </span>

        {currentIdx < questions.length - 1 ? (
          <button
            onClick={() => setCurrentIdx(prev => prev + 1)}
            className="btn btn-primary"
          >
            <span>Next</span>
            <ArrowRight size={16} />
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="btn btn-primary"
            style={{ background: 'var(--success)' }}
          >
            <CheckCircle2 size={16} />
            <span>{submitting ? 'Analyzing Responses...' : 'Submit & Generate Path'}</span>
          </button>
        )}
      </div>
    </div>
  );
}
