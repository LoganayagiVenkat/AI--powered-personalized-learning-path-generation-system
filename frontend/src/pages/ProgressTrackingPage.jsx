import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  TrendingUp,
  Award,
  Clock,
  Flame,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  BookOpen
} from 'lucide-react';
import api from '../services/api';

export default function ProgressTrackingPage({ setActiveTab, setSelectedTopicId }) {
  const [stats, setStats] = useState(null);
  const [learningPath, setLearningPath] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [dashData, pathData] = await Promise.all([
          api.getDashboardStats(),
          api.getLearningPath()
        ]);
        setStats(dashData);
        setLearningPath(pathData);
      } catch (err) {
        console.error('Error fetching progress tracking:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="page-wrapper" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <Sparkles size={36} color="#6366F1" style={{ animation: 'spin 2s linear infinite' }} />
          <p style={{ marginTop: '12px', fontWeight: 600, color: '#64748B' }}>Loading your comprehensive progress analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-wrapper">
      {/* Top Header */}
      <div className="card-gradient-border" style={{ marginBottom: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <span style={{ fontSize: '12px', fontWeight: 700, color: '#4F46E5', textTransform: 'uppercase' }}>
              Student Analytics & Metrics
            </span>
            <h1 style={{ fontSize: '24px', fontWeight: 800, color: '#0F172A', marginTop: '2px' }}>
              Progress Tracking Dashboard
            </h1>
            <p style={{ fontSize: '14px', color: '#64748B' }}>
              Real-time telemetry on time spent, quiz mastery rates, and adaptive topic completion
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ background: '#FFFBEB', border: '1px solid #FDE68A', padding: '10px 16px', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Flame size={20} color="#EA580C" />
              <div>
                <div style={{ fontSize: '11px', color: '#92400E', fontWeight: 600 }}>Active Streak</div>
                <div style={{ fontSize: '16px', fontWeight: 800, color: '#78350F' }}>{stats?.streak_days || 4} Days</div>
              </div>
            </div>

            <div style={{ background: '#EEF2FF', border: '1px solid #C7D2FE', padding: '10px 16px', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Clock size={20} color="#4F46E5" />
              <div>
                <div style={{ fontSize: '11px', color: '#4338CA', fontWeight: 600 }}>Time Invested</div>
                <div style={{ fontSize: '16px', fontWeight: 800, color: '#312E81' }}>{Math.round((stats?.total_learning_minutes || 180) / 60 * 10) / 10} hrs</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 3 Metric Cards */}
      <div className="grid-3" style={{ marginBottom: '28px' }}>
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '13px', fontWeight: 600, color: '#64748B' }}>Completion Percentage</span>
            <TrendingUp size={18} color="#4F46E5" />
          </div>
          <div style={{ fontSize: '32px', fontWeight: 800, color: '#0F172A' }}>
            {stats?.overall_progress || 0}%
          </div>
          <div style={{ height: '6px', background: '#F1F5F9', borderRadius: '9999px', margin: '10px 0 6px', overflow: 'hidden' }}>
            <div style={{ height: '100%', width: `${stats?.overall_progress || 0}%`, background: 'var(--gradient-brand)', borderRadius: '9999px' }} />
          </div>
          <span style={{ fontSize: '12px', color: '#64748B' }}>
            {stats?.completed_topics || 0} of {stats?.total_topics || 12} modules cleared
          </span>
        </div>

        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '13px', fontWeight: 600, color: '#64748B' }}>Average Quiz Score</span>
            <Award size={18} color="#059669" />
          </div>
          <div style={{ fontSize: '32px', fontWeight: 800, color: '#059669' }}>
            {stats?.avg_quiz_score || 82}%
          </div>
          <span style={{ fontSize: '12px', color: '#64748B' }}>
            Target threshold for fast-tracking: 85%
          </span>
        </div>

        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '13px', fontWeight: 600, color: '#64748B' }}>Next Focus Topic</span>
            <BookOpen size={18} color="#D97706" />
          </div>
          <div style={{ fontSize: '18px', fontWeight: 800, color: '#0F172A', marginTop: '6px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {stats?.current_topic || 'Python Fundamentals'}
          </div>
          <span style={{ fontSize: '12px', color: '#D97706', fontWeight: 600 }}>
            {stats?.pending_topics || 0} modules remaining on roadmap
          </span>
        </div>
      </div>

      {/* Topic-by-Topic Status Table */}
      <div className="card" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '17px', fontWeight: 800, color: '#0F172A', marginBottom: '16px' }}>
          Curriculum Topic Master List & Status
        </h3>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '13px' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #E2E8F0', color: '#64748B', fontWeight: 700 }}>
                <th style={{ padding: '12px 14px' }}>#</th>
                <th style={{ padding: '12px 14px' }}>Topic Title</th>
                <th style={{ padding: '12px 14px' }}>Category</th>
                <th style={{ padding: '12px 14px' }}>Difficulty</th>
                <th style={{ padding: '12px 14px' }}>Status</th>
                <th style={{ padding: '12px 14px', textAlign: 'right' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {learningPath?.topics?.map((t, idx) => (
                <tr key={t.id} style={{ borderBottom: '1px solid #F1F5F9' }}>
                  <td style={{ padding: '12px 14px', fontWeight: 700, color: '#64748B' }}>{t.sequence_order || idx + 1}</td>
                  <td style={{ padding: '12px 14px', fontWeight: 600, color: '#0F172A' }}>{t.title}</td>
                  <td style={{ padding: '12px 14px', color: '#475569' }}>{t.category}</td>
                  <td style={{ padding: '12px 14px' }}>
                    <span style={{
                      fontWeight: 600,
                      color: t.difficulty === 'Advanced' ? '#DC2626' : (t.difficulty === 'Intermediate' ? '#D97706' : '#059669')
                    }}>
                      {t.difficulty}
                    </span>
                  </td>
                  <td style={{ padding: '12px 14px' }}>
                    {t.status === 'completed' && <span className="badge badge-green">Completed</span>}
                    {t.status === 'in_progress' && <span className="badge badge-purple">In Progress</span>}
                    {t.status === 'review_needed' && <span className="badge badge-amber">Review Needed</span>}
                    {t.status === 'pending' && <span className="badge" style={{ background: '#F1F5F9', color: '#64748B' }}>Pending</span>}
                  </td>
                  <td style={{ padding: '12px 14px', textAlign: 'right' }}>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => {
                        setSelectedTopicId(t.id);
                        setActiveTab('topics');
                      }}
                    >
                      Study
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
