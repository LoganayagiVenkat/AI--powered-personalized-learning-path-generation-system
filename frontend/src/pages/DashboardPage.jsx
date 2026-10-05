import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  Award,
  BookOpen,
  Clock,
  Flame,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  ArrowRight,
  Brain,
  Users,
  Compass
} from 'lucide-react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function DashboardPage({ setActiveTab, setSelectedTopicId }) {
  const { user, profile } = useAuth();
  const [stats, setStats] = useState(null);
  const [learningPath, setLearningPath] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const [dashData, pathData] = await Promise.all([
          api.getDashboardStats(),
          api.getLearningPath()
        ]);
        setStats(dashData);
        setLearningPath(pathData);
      } catch (err) {
        console.error('Error loading dashboard:', err);
      } finally {
        setLoading(false);
      }
    };
    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="page-wrapper" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <Sparkles size={36} color="#6366F1" style={{ animation: 'spin 2s linear infinite' }} />
          <p style={{ marginTop: '12px', fontWeight: 600, color: '#64748B' }}>Loading your personalized learning dashboard...</p>
        </div>
      </div>
    );
  }

  const activeTopic = learningPath?.topics?.find(t => t.status === 'in_progress' || t.status === 'review_needed') || learningPath?.topics?.[0];

  return (
    <div className="page-wrapper">
      {/* Welcome Banner */}
      <div style={{
        background: 'linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%)',
        borderRadius: '24px',
        padding: '32px 36px',
        color: 'white',
        marginBottom: '28px',
        position: 'relative',
        overflow: 'hidden',
        boxShadow: '0 20px 25px -5px rgba(49, 46, 129, 0.2)'
      }}>
        {/* Decorative background glow */}
        <div style={{
          position: 'absolute',
          right: '-50px',
          top: '-50px',
          width: '280px',
          height: '280px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(139, 92, 246, 0.4) 0%, rgba(99, 102, 241, 0) 70%)',
          pointerEvents: 'none'
        }} />

        <div style={{ maxWidth: '750px', position: 'relative', zIndex: 2 }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'rgba(255, 255, 255, 0.15)', padding: '4px 12px', borderRadius: '9999px', fontSize: '12px', fontWeight: 600, marginBottom: '14px', backdropFilter: 'blur(4px)' }}>
            <Sparkles size={14} color="#FDE047" /> AI Powered Personalized Roadmap
          </div>
          <h1 style={{ fontSize: '28px', fontWeight: 800, lineHeight: 1.25, color: '#FFFFFF', marginBottom: '8px' }}>
            Welcome back, {user?.name || 'Alex'}!
          </h1>
          <p style={{ fontSize: '15px', color: '#E0E7FF', lineHeight: 1.6, marginBottom: '22px' }}>
            Your custom path to <strong style={{ color: '#FBCFE8' }}>{user?.target_job_role || 'Data Scientist'}</strong> is actively adapting.
            Master your current focus module to unlock downstream machine learning pipelines.
          </p>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '14px' }}>
            {activeTopic && (
              <button
                className="btn btn-primary"
                onClick={() => {
                  setSelectedTopicId(activeTopic.id);
                  setActiveTab('topics');
                }}
                style={{ background: 'white', color: '#4338CA', fontWeight: 700 }}
              >
                <span>Continue: {activeTopic.title}</span>
                <ArrowRight size={16} />
              </button>
            )}
            <button
              className="btn btn-secondary"
              onClick={() => setActiveTab('learning-path')}
              style={{ background: 'rgba(255, 255, 255, 0.12)', color: 'white', borderColor: 'rgba(255, 255, 255, 0.25)' }}
            >
              <span>View Full AI Path</span>
            </button>
          </div>
        </div>
      </div>

      {/* Top 4 KPI Metric Cards */}
      <div className="grid-4" style={{ marginBottom: '28px' }}>
        {/* Overall Progress */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <span style={{ fontSize: '13px', fontWeight: 600, color: '#64748B' }}>Overall Roadmap</span>
            <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: '#EEF2FF', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <TrendingUp size={18} color="#4F46E5" />
            </div>
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#0F172A' }}>
            {stats?.overall_progress || 0}%
          </div>
          <div style={{ height: '6px', background: '#F1F5F9', borderRadius: '9999px', margin: '10px 0 6px', overflow: 'hidden' }}>
            <div style={{ height: '100%', width: `${stats?.overall_progress || 0}%`, background: 'var(--gradient-brand)', borderRadius: '9999px' }} />
          </div>
          <span style={{ fontSize: '12px', color: '#64748B' }}>
            {stats?.completed_topics || 0} of {stats?.total_topics || 12} topics mastered
          </span>
        </div>

        {/* Current Active Topic */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <span style={{ fontSize: '13px', fontWeight: 600, color: '#64748B' }}>Current Focus</span>
            <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: '#FEF3C7', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <BookOpen size={18} color="#D97706" />
            </div>
          </div>
          <div style={{ fontSize: '16px', fontWeight: 800, color: '#0F172A', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {stats?.current_topic || 'Python Fundamentals'}
          </div>
          <div style={{ marginTop: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="badge badge-amber">In Progress</span>
            <span style={{ fontSize: '12px', color: '#64748B' }}>{stats?.pending_topics || 0} pending</span>
          </div>
        </div>

        {/* Learning Streak */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <span style={{ fontSize: '13px', fontWeight: 600, color: '#64748B' }}>Study Streak</span>
            <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: '#FFEDD5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Flame size={18} color="#EA580C" />
            </div>
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#0F172A' }}>
            {stats?.streak_days || 4} Days
          </div>
          <span style={{ fontSize: '12px', color: '#059669', fontWeight: 600 }}>
            🔥 Consistent daily progress
          </span>
        </div>

        {/* Average Quiz Score */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <span style={{ fontSize: '13px', fontWeight: 600, color: '#64748B' }}>Avg Quiz Mastery</span>
            <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: '#ECFDF5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Award size={18} color="#059669" />
            </div>
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#0F172A' }}>
            {stats?.avg_quiz_score || 82}%
          </div>
          <span style={{ fontSize: '12px', color: '#64748B' }}>
            {stats?.total_learning_minutes || 180} min total time invested
          </span>
        </div>
      </div>

      {/* Main Grid: Peer Cohort & AI Path Preview */}
      <div className="grid-2" style={{ marginBottom: '28px' }}>
        {/* K-Means Peer Cohort Card */}
        <div className="card-gradient-border">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <div style={{ width: '40px', height: '40px', borderRadius: '10px', background: 'var(--primary-light)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Users size={20} color="#4F46E5" />
            </div>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: 800 }}>AI Student Clustering Cohort</h3>
              <p style={{ fontSize: '12px', color: '#64748B' }}>K-Means Clustering based on assessment & skills</p>
            </div>
          </div>

          <div style={{ background: '#F8FAFC', borderRadius: '12px', padding: '16px', border: '1px solid #E2E8F0', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ fontSize: '15px', fontWeight: 800, color: '#4338CA' }}>
                {stats?.cohort?.cohort_name || 'Algorithmic Builder'}
              </span>
              <span className="badge badge-purple">
                Cluster #{stats?.cohort?.cluster_id ?? 1}
              </span>
            </div>
            <p style={{ fontSize: '13px', color: '#334155', lineHeight: 1.5, marginBottom: '12px' }}>
              {stats?.cohort?.description || 'Proficient in programming fundamentals; accelerating through statistical modeling and real-world datasets.'}
            </p>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', fontSize: '12px', color: '#64748B', borderTop: '1px solid #E2E8F0', paddingTop: '10px' }}>
              <div>Pacing: <strong style={{ color: '#0F172A' }}>{stats?.cohort?.pacing || 'Accelerated'}</strong></div>
              <div>Target: <strong style={{ color: '#0F172A' }}>{stats?.cohort?.recommended_daily_target_minutes || 60}m/day</strong></div>
            </div>
          </div>

          <div className="ai-reasoning-box">
            <div className="ai-reasoning-title">
              <Sparkles size={14} /> Cohort Strategy Recommendation
            </div>
            <p className="ai-reasoning-text">
              {stats?.cohort?.learning_strategy || 'Emphasize end-to-end dataset wrangling, comparative algorithmic modeling, and Kaggle-style mini-challenges.'}
            </p>
          </div>
        </div>

        {/* Strong vs Weak Skills Matrix */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '18px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Brain size={20} color="#6366F1" />
              <h3 style={{ fontSize: '16px', fontWeight: 800 }}>Skill Mastery Distribution</h3>
            </div>
            <button
              onClick={() => setActiveTab('skill-gap')}
              className="btn btn-sm btn-secondary"
            >
              Analyze Gaps
            </button>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#059669', textTransform: 'uppercase', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <CheckCircle2 size={15} /> Identified Strong Foundations
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {stats?.strong_skills?.map((s, idx) => (
                <span key={idx} className="badge badge-green" style={{ fontSize: '12px', padding: '6px 12px' }}>
                  {s}
                </span>
              ))}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#DC2626', textTransform: 'uppercase', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <AlertCircle size={15} /> Priority Focus & Weak Areas
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {stats?.weak_skills?.map((s, idx) => (
                <span key={idx} className="badge badge-amber" style={{ fontSize: '12px', padding: '6px 12px' }}>
                  {s}
                </span>
              ))}
            </div>
          </div>

          <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid #E2E8F0' }}>
            <button
              onClick={() => setActiveTab('assessment')}
              className="btn btn-primary"
              style={{ width: '100%', fontSize: '13px' }}
            >
              <span>Take Diagnostic Skill Assessment</span>
              <ArrowRight size={15} />
            </button>
          </div>
        </div>
      </div>

      {/* Weekly Activity Trend */}
      <div className="card">
        <h3 style={{ fontSize: '16px', fontWeight: 800, marginBottom: '6px' }}>Weekly Learning Hours Trend</h3>
        <p style={{ fontSize: '13px', color: '#64748B', marginBottom: '20px' }}>Total hours dedicated to curriculum lessons & quizzes</p>

        <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', height: '140px', padding: '0 20px', borderBottom: '1px solid #E2E8F0' }}>
          {stats?.activity_chart?.map((item, idx) => {
            const heightPct = Math.min(100, (item.hours / 3.0) * 100);
            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', width: '40px' }}>
                <span style={{ fontSize: '11px', fontWeight: 700, color: '#4F46E5' }}>{item.hours}h</span>
                <div style={{
                  width: '28px',
                  height: `${Math.max(12, heightPct)}px`,
                  background: 'var(--gradient-brand)',
                  borderRadius: '6px 6px 0 0',
                  transition: 'height 0.3s ease'
                }} />
                <span style={{ fontSize: '12px', color: '#64748B', fontWeight: 600, marginTop: '4px' }}>{item.day}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
