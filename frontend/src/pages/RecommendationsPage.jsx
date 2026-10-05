import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  BookOpen,
  Award,
  Code2,
  FolderGit2,
  ExternalLink,
  ArrowRight
} from 'lucide-react';
import api from '../services/api';

export default function RecommendationsPage({ setActiveTab, setSelectedTopicId }) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecs = async () => {
      try {
        setLoading(true);
        const data = await api.getRecommendations();
        setRecommendations(data);
      } catch (err) {
        console.error('Error fetching recommendations:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchRecs();
  }, []);

  if (loading) {
    return (
      <div className="page-wrapper" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <Sparkles size={36} color="#6366F1" style={{ animation: 'spin 2s linear infinite' }} />
          <p style={{ marginTop: '12px', fontWeight: 600, color: '#64748B' }}>Mining content recommendations based on your profile...</p>
        </div>
      </div>
    );
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'topic': return <BookOpen size={18} color="#4F46E5" />;
      case 'project': return <FolderGit2 size={18} color="#059669" />;
      case 'quiz': return <Award size={18} color="#D97706" />;
      case 'course': return <ExternalLink size={18} color="#7C3AED" />;
      default: return <Sparkles size={18} color="#6366F1" />;
    }
  };

  return (
    <div className="page-wrapper">
      {/* Banner */}
      <div className="card-gradient-border" style={{ marginBottom: '28px' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'var(--primary-light)', padding: '4px 12px', borderRadius: '9999px', fontSize: '12px', fontWeight: 700, color: '#4F46E5', marginBottom: '8px' }}>
          <Sparkles size={14} /> AI Recommendation Engine
        </div>
        <h1 style={{ fontSize: '24px', fontWeight: 800, color: '#0F172A' }}>
          Personalized Multi-Modal Recommendations
        </h1>
        <p style={{ fontSize: '14px', color: '#64748B', marginTop: '4px' }}>
          Tailored learning topics, hands-on projects, industry courses, and quizzes calibrated to your career trajectory.
        </p>
      </div>

      {/* Recommendations Grid */}
      <div className="grid-2">
        {recommendations.map((rec, idx) => (
          <div key={idx} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: '#F8FAFC', border: '1px solid #E2E8F0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {getTypeIcon(rec.item_type)}
                  </div>
                  <span className="badge badge-purple" style={{ textTransform: 'capitalize' }}>
                    {rec.badge || rec.item_type}
                  </span>
                </div>
                {rec.score && (
                  <span style={{ fontSize: '12px', fontWeight: 700, color: '#4F46E5' }}>
                    Match: {Math.round(rec.score * 100)}%
                  </span>
                )}
              </div>

              <h3 style={{ fontSize: '17px', fontWeight: 800, color: '#0F172A', marginBottom: '8px' }}>
                {rec.item_title}
              </h3>

              <div className="ai-reasoning-box" style={{ marginBottom: '16px' }}>
                <div className="ai-reasoning-title">
                  <Sparkles size={13} /> Why Recommended
                </div>
                <p className="ai-reasoning-text">
                  {rec.reasoning}
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', paddingTop: '12px', borderTop: '1px solid #F1F5F9' }}>
              {rec.item_id ? (
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => {
                    setSelectedTopicId(rec.item_id);
                    setActiveTab(rec.item_type === 'quiz' ? 'quiz' : 'topics');
                  }}
                >
                  <span>{rec.item_type === 'quiz' ? 'Take Quiz' : 'Open Topic'}</span>
                  <ArrowRight size={14} />
                </button>
              ) : (
                <a
                  href={rec.action_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-secondary btn-sm"
                >
                  <span>Explore External Resource</span>
                  <ExternalLink size={14} />
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
