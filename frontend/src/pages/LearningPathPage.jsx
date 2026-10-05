import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  CheckCircle2,
  Clock,
  ArrowRight,
  RefreshCw,
  AlertTriangle,
  BookOpen,
  HelpCircle,
  TrendingUp,
  BrainCircuit,
  Filter
} from 'lucide-react';
import api from '../services/api';

export default function LearningPathPage({ setActiveTab, setSelectedTopicId }) {
  const [pathData, setPathData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);
  const [statusFilter, setStatusFilter] = useState('all');

  const fetchPath = async () => {
    try {
      setLoading(true);
      const data = await api.getLearningPath();
      setPathData(data);
    } catch (err) {
      console.error('Error loading learning path:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPath();
  }, []);

  const handleRegenerate = async () => {
    try {
      setRegenerating(true);
      const updated = await api.generateLearningPath();
      setPathData(updated);
    } catch (err) {
      console.error('Error re-generating path:', err);
    } finally {
      setRegenerating(false);
    }
  };

  const filteredTopics = (pathData?.topics || []).filter((topic) => {
    if (statusFilter === 'all') return true;
    if (statusFilter === 'in_progress') return topic.status === 'in_progress' || topic.status === 'review_needed';
    if (statusFilter === 'completed') return topic.status === 'completed';
    if (statusFilter === 'pending') return topic.status === 'pending';
    return true;
  });

  if (loading) {
    return (
      <div className="page-wrapper" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <Sparkles size={36} color="#6366F1" style={{ animation: 'spin 2s linear infinite' }} />
          <p style={{ marginTop: '12px', fontWeight: 600, color: '#64748B' }}>Computing DAG topological sequence and AI recommendations...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-wrapper">
      {/* Top Header Card */}
      <div className="card-gradient-border" style={{ marginBottom: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'var(--primary-light)', padding: '4px 12px', borderRadius: '9999px', fontSize: '12px', fontWeight: 700, color: '#4F46E5', marginBottom: '8px' }}>
              <BrainCircuit size={14} /> DAG Topological Prerequisite Sequencing
            </div>
            <h1 style={{ fontSize: '24px', fontWeight: 800, color: '#0F172A' }}>
              {pathData?.title || 'Personalized AI Learning Roadmap'}
            </h1>
            <p style={{ fontSize: '14px', color: '#64748B', marginTop: '4px' }}>
              Target Role: <strong style={{ color: '#4F46E5' }}>{pathData?.target_role || 'Data Scientist'}</strong> • {pathData?.total_topics || 0} Modules Sequenced
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <button
              onClick={handleRegenerate}
              disabled={regenerating}
              className="btn btn-secondary"
              style={{ fontSize: '13px' }}
            >
              <RefreshCw size={14} className={regenerating ? 'spin' : ''} />
              <span>{regenerating ? 'Recalculating...' : 'Regenerate with AI'}</span>
            </button>
          </div>
        </div>

        {/* Global Progress Bar */}
        <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid #E2E8F0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', fontWeight: 600, marginBottom: '6px' }}>
            <span style={{ color: '#64748B' }}>Path Completion</span>
            <span style={{ color: '#4F46E5' }}>{pathData?.overall_progress || 0}% ({pathData?.completed_topics || 0} completed)</span>
          </div>
          <div style={{ height: '8px', background: '#F1F5F9', borderRadius: '9999px', overflow: 'hidden' }}>
            <div style={{
              height: '100%',
              width: `${pathData?.overall_progress || 0}%`,
              background: 'var(--gradient-brand)',
              borderRadius: '9999px',
              transition: 'width 0.4s ease'
            }} />
          </div>
        </div>

        {/* Algorithmic Engine Reasoning Summary */}
        {pathData?.ai_reasoning && (
          <div className="ai-reasoning-box" style={{ marginTop: '16px' }}>
            <div className="ai-reasoning-title">
              <Sparkles size={14} /> AI Recommendation Engine Logic
            </div>
            <p className="ai-reasoning-text">
              {pathData.ai_reasoning}
            </p>
          </div>
        )}
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
        <span style={{ fontSize: '13px', fontWeight: 600, color: '#64748B', display: 'flex', alignItems: 'center', gap: '4px' }}>
          <Filter size={14} /> Filter:
        </span>
        {['all', 'in_progress', 'pending', 'completed'].map((tab) => (
          <button
            key={tab}
            onClick={() => setStatusFilter(tab)}
            style={{
              padding: '6px 14px',
              borderRadius: '9999px',
              border: 'none',
              background: statusFilter === tab ? 'var(--primary)' : '#E2E8F0',
              color: statusFilter === tab ? 'white' : '#475569',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
              textTransform: 'capitalize'
            }}
          >
            {tab.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Sequential Timeline List */}
      <div className="timeline-list">
        {filteredTopics.map((topic) => {
          const isCompleted = topic.status === 'completed';
          const isInProgress = topic.status === 'in_progress';
          const isReviewNeeded = topic.status === 'review_needed';

          return (
            <div
              key={topic.id}
              className={`timeline-node ${topic.status}`}
            >
              <div className="timeline-bullet">
                {isCompleted ? <CheckCircle2 size={14} /> : topic.sequence_order}
              </div>

              <div
                className="card"
                style={{
                  background: isInProgress ? '#FFFFFF' : (isCompleted ? '#F8FAFC' : '#FFFFFF'),
                  borderColor: isInProgress ? '#818CF8' : (isReviewNeeded ? '#F59E0B' : '#E2E8F0'),
                  boxShadow: isInProgress ? '0 10px 25px -5px rgba(99, 102, 241, 0.15)' : 'var(--shadow-sm)'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
                  <div style={{ flex: 1, minWidth: '280px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                      <span className="badge badge-purple" style={{ fontSize: '11px' }}>
                        Step {topic.sequence_order}
                      </span>
                      <span className="badge badge-blue" style={{ fontSize: '11px' }}>
                        {topic.category}
                      </span>
                      <span style={{ fontSize: '12px', color: '#64748B', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Clock size={13} /> {topic.estimated_learning_time || `${topic.estimated_hours} hours`}
                      </span>
                      {topic.difficulty && (
                        <span style={{
                          fontSize: '11px',
                          fontWeight: 700,
                          color: topic.difficulty === 'Advanced' ? '#DC2626' : (topic.difficulty === 'Intermediate' ? '#D97706' : '#059669')
                        }}>
                          • {topic.difficulty}
                        </span>
                      )}
                    </div>

                    <h3 style={{ fontSize: '17px', fontWeight: 800, color: '#0F172A', marginBottom: '6px' }}>
                      {topic.title}
                    </h3>
                  </div>

                  {/* Status Badge & Action Buttons */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {isCompleted && <span className="badge badge-green">Completed</span>}
                    {isInProgress && <span className="badge badge-purple">In Progress</span>}
                    {isReviewNeeded && <span className="badge badge-amber">Remedial Review</span>}
                    {topic.status === 'pending' && <span className="badge" style={{ background: '#F1F5F9', color: '#64748B' }}>Pending</span>}

                    <button
                      className="btn btn-primary btn-sm"
                      onClick={() => {
                        setSelectedTopicId(topic.id);
                        setActiveTab('topics');
                      }}
                    >
                      <BookOpen size={14} />
                      <span>{isCompleted ? 'Review Lesson' : 'Start Study'}</span>
                    </button>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => {
                        setSelectedTopicId(topic.id);
                        setActiveTab('quiz');
                      }}
                    >
                      <span>Take Quiz</span>
                    </button>
                  </div>
                </div>

                {/* AI Reasoning Container */}
                {topic.recommended_reason && (
                  <div className="ai-reasoning-box">
                    <div className="ai-reasoning-title">
                      <Sparkles size={13} /> Why AI Recommended This Topic
                    </div>
                    <p className="ai-reasoning-text">
                      {topic.recommended_reason}
                    </p>
                  </div>
                )}

                {/* Random Forest Predictive Insights */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '18px',
                  marginTop: '12px',
                  paddingTop: '10px',
                  borderTop: '1px solid #F1F5F9',
                  fontSize: '12px',
                  color: '#64748B',
                  flexWrap: 'wrap'
                }}>
                  {topic.predicted_pass_prob && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                      <TrendingUp size={14} color="#4F46E5" />
                      <span>Predicted Quiz Pass Probability: <strong style={{ color: '#0F172A' }}>{topic.predicted_pass_prob}%</strong></span>
                    </div>
                  )}
                  {topic.cosine_similarity && (
                    <div>
                      <span>Role Cosine Similarity: <strong style={{ color: '#4F46E5' }}>{topic.cosine_similarity}</strong></span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
