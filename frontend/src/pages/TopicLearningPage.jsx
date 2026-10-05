import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  CheckCircle2,
  Clock,
  Sparkles,
  ExternalLink,
  Code2,
  FileText,
  Award,
  ArrowRight,
  ChevronRight,
  Layers
} from 'lucide-react';
import api from '../services/api';

export default function TopicLearningPage({ topicId, setActiveTab, setSelectedTopicId }) {
  const [topic, setTopic] = useState(null);
  const [activeSubtopicIdx, setActiveSubtopicIdx] = useState(0);
  const [loading, setLoading] = useState(true);
  const [markingComplete, setMarkingComplete] = useState(false);
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    const fetchTopic = async () => {
      try {
        setLoading(true);
        const targetId = topicId || 1;
        const data = await api.getTopicDetail(targetId);
        setTopic(data);
      } catch (err) {
        console.error('Error fetching topic:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchTopic();
  }, [topicId]);

  const handleMarkComplete = async () => {
    try {
      setMarkingComplete(true);
      await api.updateProgress(topic.id, topic.subtopics?.[activeSubtopicIdx]?.id, 25, 100);
      setCompleted(true);
    } catch (err) {
      console.error('Error marking completed:', err);
    } finally {
      setMarkingComplete(false);
    }
  };

  if (loading) {
    return (
      <div className="page-wrapper" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <Sparkles size={36} color="#6366F1" style={{ animation: 'spin 2s linear infinite' }} />
          <p style={{ marginTop: '12px', fontWeight: 600, color: '#64748B' }}>Loading lesson content and exercises...</p>
        </div>
      </div>
    );
  }

  if (!topic) {
    return (
      <div className="page-wrapper">
        <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
          <h3>Topic not found</h3>
          <button className="btn btn-primary" onClick={() => setActiveTab('learning-path')} style={{ marginTop: '16px' }}>
            Back to Learning Path
          </button>
        </div>
      </div>
    );
  }

  const activeSubtopic = topic.subtopics?.[activeSubtopicIdx] || topic.subtopics?.[0];

  return (
    <div className="page-wrapper">
      {/* Header Banner */}
      <div className="card-gradient-border" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <span className="badge badge-purple">{topic.category}</span>
              <span className="badge badge-blue">{topic.difficulty}</span>
              <span style={{ fontSize: '13px', color: '#64748B', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Clock size={14} /> Estimated: {topic.estimated_hours} Hours
              </span>
            </div>
            <h1 style={{ fontSize: '26px', fontWeight: 800, color: '#0F172A', marginBottom: '6px' }}>
              {topic.title}
            </h1>
            <p style={{ fontSize: '14px', color: '#64748B', maxWidth: '800px', lineHeight: 1.6 }}>
              {topic.description}
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <button
              onClick={handleMarkComplete}
              disabled={markingComplete || completed}
              className="btn btn-secondary"
              style={{ background: completed ? '#ECFDF5' : 'white', color: completed ? '#059669' : '#0F172A' }}
            >
              <CheckCircle2 size={16} color={completed ? '#059669' : '#64748B'} />
              <span>{completed ? 'Completed' : (markingComplete ? 'Saving...' : 'Mark Completed')}</span>
            </button>

            <button
              onClick={() => {
                setSelectedTopicId(topic.id);
                setActiveTab('quiz');
              }}
              className="btn btn-secondary"
              title="Interactive 3D Revision Flashcards"
            >
              <Layers size={16} color="#6366F1" />
              <span>Flashcards</span>
            </button>

            <button
              onClick={() => {
                setSelectedTopicId(topic.id);
                setActiveTab('quiz');
              }}
              className="btn btn-primary"
            >
              <Sparkles size={16} />
              <span>AI Quiz & Assessment</span>
              <ArrowRight size={16} />
            </button>
          </div>
        </div>

        {/* Key Concepts Chips */}
        <div style={{ marginTop: '18px', paddingTop: '14px', borderTop: '1px solid #E2E8F0', display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '12px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Key Concepts:</span>
          {topic.concepts?.map((c, idx) => (
            <span key={idx} style={{
              background: '#F1F5F9',
              color: '#334155',
              padding: '4px 10px',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 600
            }}>
              {c}
            </span>
          ))}
        </div>
      </div>

      {/* Main Content Layout: Sidebar + Lesson Viewer */}
      <div style={{ display: 'flex', gap: '24px', alignItems: 'flex-start', flexWrap: 'wrap' }}>
        {/* Left Subtopics Nav */}
        <div style={{ width: '280px', flexShrink: 0 }}>
          <div className="card" style={{ padding: '16px' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#0F172A', marginBottom: '12px', paddingLeft: '8px' }}>
              Lesson Subtopics ({topic.subtopics?.length || 0})
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {topic.subtopics?.map((st, idx) => (
                <button
                  key={st.id}
                  onClick={() => setActiveSubtopicIdx(idx)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '10px 12px',
                    borderRadius: '8px',
                    border: 'none',
                    background: activeSubtopicIdx === idx ? 'var(--primary-light)' : 'transparent',
                    color: activeSubtopicIdx === idx ? 'var(--primary)' : '#475569',
                    fontFamily: 'inherit',
                    fontSize: '13px',
                    fontWeight: activeSubtopicIdx === idx ? 700 : 500,
                    cursor: 'pointer',
                    textAlign: 'left'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '11px', opacity: 0.7 }}>0{idx + 1}.</span>
                    <span>{st.title}</span>
                  </div>
                  {activeSubtopicIdx === idx && <ChevronRight size={14} />}
                </button>
              ))}
            </div>
          </div>

          {/* Curated Resources Card */}
          <div className="card" style={{ marginTop: '20px', padding: '20px' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#0F172A', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <ExternalLink size={15} color="#4F46E5" /> Curated Resources
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {topic.resources?.map((res, idx) => (
                <a
                  key={idx}
                  href={res.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    textDecoration: 'none',
                    background: '#F8FAFC',
                    border: '1px solid #E2E8F0',
                    borderRadius: '8px',
                    padding: '10px 12px',
                    display: 'block',
                    transition: 'border-color 0.2s ease'
                  }}
                >
                  <div style={{ fontSize: '12px', fontWeight: 700, color: '#4F46E5', marginBottom: '2px' }}>
                    {res.title}
                  </div>
                  <span style={{ fontSize: '11px', color: '#64748B' }}>
                    {res.type} ↗
                  </span>
                </a>
              ))}
            </div>
          </div>
        </div>

        {/* Right Active Subtopic Learning Panel */}
        <div style={{ flex: 1, minWidth: '320px' }}>
          {activeSubtopic ? (
            <div className="card" style={{ padding: '32px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <span className="badge badge-purple" style={{ fontSize: '11px' }}>
                  Subtopic 0{activeSubtopicIdx + 1}
                </span>
              </div>
              <h2 style={{ fontSize: '22px', fontWeight: 800, color: '#0F172A', marginBottom: '14px' }}>
                {activeSubtopic.title}
              </h2>

              <p style={{ fontSize: '15px', color: '#334155', lineHeight: 1.7, marginBottom: '24px' }}>
                {activeSubtopic.summary}
              </p>

              {/* Rich Lesson Content */}
              <div style={{
                background: '#F8FAFC',
                border: '1px solid #E2E8F0',
                borderRadius: '12px',
                padding: '24px',
                fontSize: '14px',
                color: '#1E293B',
                lineHeight: 1.8,
                marginBottom: '28px'
              }}>
                <div style={{ fontWeight: 700, fontSize: '15px', marginBottom: '10px', color: '#0F172A' }}>
                  Interactive Study Breakdown:
                </div>
                <p style={{ marginBottom: '14px' }}>
                  {activeSubtopic.content}
                </p>
                <div style={{
                  background: '#0F172A',
                  color: '#38BDF8',
                  borderRadius: '8px',
                  padding: '16px',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '13px',
                  overflowX: 'auto'
                }}>
                  {`# Example code for ${topic.title}\nimport numpy as np\n\ndef execute_pipeline(data):\n    print("Executing optimized algorithmic step for: ${activeSubtopic.title}")\n    return np.array(data) * 2\n\nresult = execute_pipeline([10, 20, 30])\nprint("Pipeline output:", result)`}
                </div>
              </div>

              {/* Hands-on Practice Exercises */}
              <div style={{ borderTop: '1px solid #E2E8F0', paddingTop: '20px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#0F172A', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Code2 size={18} color="#6366F1" /> Hands-On Practice Exercises
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {topic.practice_exercises?.map((ex, idx) => (
                    <div
                      key={idx}
                      style={{
                        display: 'flex',
                        alignItems: 'flex-start',
                        gap: '12px',
                        background: '#FFFFFF',
                        border: '1px solid #E2E8F0',
                        borderRadius: '10px',
                        padding: '14px 16px'
                      }}
                    >
                      <span style={{
                        width: '24px',
                        height: '24px',
                        borderRadius: '50%',
                        background: 'var(--primary-light)',
                        color: 'var(--primary)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '12px',
                        fontWeight: 700,
                        flexShrink: 0
                      }}>
                        {idx + 1}
                      </span>
                      <span style={{ fontSize: '14px', color: '#334155', lineHeight: 1.5 }}>
                        {ex}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="card">No subtopics available</div>
          )}
        </div>
      </div>
    </div>
  );
}
