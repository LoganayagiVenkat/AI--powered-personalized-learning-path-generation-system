import React, { useState, useEffect } from 'react';
import {
  Split,
  Sparkles,
  AlertTriangle,
  CheckCircle2,
  BookOpen,
  ArrowRight,
  TrendingUp,
  Target
} from 'lucide-react';
import api from '../services/api';

export default function SkillGapPage({ setActiveTab, setSelectedTopicId }) {
  const [gapData, setGapData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGaps = async () => {
      try {
        setLoading(true);
        const data = await api.getSkillGaps();
        setGapData(data);
      } catch (err) {
        console.error('Error fetching skill gaps:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchGaps();
  }, []);

  if (loading) {
    return (
      <div className="page-wrapper" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <Sparkles size={36} color="#6366F1" style={{ animation: 'spin 2s linear infinite' }} />
          <p style={{ marginTop: '12px', fontWeight: 600, color: '#64748B' }}>Comparing your competencies against target industry requirements...</p>
        </div>
      </div>
    );
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Critical':
        return <span className="badge badge-red">Critical Gap</span>;
      case 'Moderate':
        return <span className="badge badge-amber">Moderate Gap</span>;
      case 'Met':
        return <span className="badge badge-green">Requirement Met</span>;
      case 'Advanced':
        return <span className="badge badge-purple">Exceeds Requirement</span>;
      default:
        return <span className="badge badge-blue">{status}</span>;
    }
  };

  const getLevelColor = (level) => {
    if (level === 'Advanced') return '#7C3AED';
    if (level === 'Intermediate') return '#4F46E5';
    return '#059669';
  };

  return (
    <div className="page-wrapper">
      {/* Target Goal Summary Banner */}
      <div className="card-gradient-border" style={{ marginBottom: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '20px' }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'var(--primary-light)', padding: '4px 12px', borderRadius: '9999px', fontSize: '12px', fontWeight: 700, color: '#4F46E5', marginBottom: '8px' }}>
              <Target size={14} /> Career Requirement Matrix
            </div>
            <h1 style={{ fontSize: '24px', fontWeight: 800, color: '#0F172A' }}>
              Skill Gap Analysis: {gapData?.target_role || 'Data Scientist'}
            </h1>
            <p style={{ fontSize: '14px', color: '#64748B', maxWidth: '680px', marginTop: '4px' }}>
              {gapData?.career_description || 'Comparing student current evaluated proficiencies against target market job competencies.'}
            </p>
          </div>

          {/* Readiness Score Ring */}
          <div style={{
            background: 'var(--gradient-soft)',
            border: '1px solid #C7D2FE',
            borderRadius: '16px',
            padding: '16px 24px',
            textAlign: 'center',
            minWidth: '180px'
          }}>
            <span style={{ fontSize: '12px', fontWeight: 700, color: '#4338CA', textTransform: 'uppercase' }}>
              Role Readiness
            </span>
            <div style={{ fontSize: '32px', fontWeight: 800, color: '#4F46E5', marginTop: '2px' }}>
              {gapData?.readiness_percentage || 45}%
            </div>
            <span style={{ fontSize: '11px', color: '#64748B' }}>
              {gapData?.met_skills_count || 1} of {gapData?.gaps?.length || 5} skills verified
            </span>
          </div>
        </div>

        {/* 3 Metric Pills */}
        <div className="grid-3" style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid #E2E8F0' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: '#FEF2F2', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <AlertTriangle size={16} color="#DC2626" />
            </div>
            <div>
              <div style={{ fontSize: '16px', fontWeight: 800, color: '#DC2626' }}>{gapData?.critical_gaps_count || 0}</div>
              <div style={{ fontSize: '12px', color: '#64748B' }}>Critical Gaps (Priority)</div>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: '#FFFBEB', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <TrendingUp size={16} color="#D97706" />
            </div>
            <div>
              <div style={{ fontSize: '16px', fontWeight: 800, color: '#D97706' }}>{gapData?.moderate_gaps_count || 0}</div>
              <div style={{ fontSize: '12px', color: '#64748B' }}>Moderate Gaps</div>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: '#ECFDF5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CheckCircle2 size={16} color="#059669" />
            </div>
            <div>
              <div style={{ fontSize: '16px', fontWeight: 800, color: '#059669' }}>{gapData?.met_skills_count || 0}</div>
              <div style={{ fontSize: '12px', color: '#64748B' }}>Skills Met / Advanced</div>
            </div>
          </div>
        </div>
      </div>

      {/* Comparison Cards Grid */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {gapData?.gaps?.map((item, idx) => (
          <div key={idx} className="card" style={{ padding: '20px 24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px', marginBottom: '14px' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <h3 style={{ fontSize: '17px', fontWeight: 800, color: '#0F172A' }}>
                    {item.skill_name}
                  </h3>
                  <span className="badge badge-purple" style={{ fontSize: '11px' }}>
                    {item.category}
                  </span>
                </div>
              </div>

              <div>
                {getStatusBadge(item.gap_status)}
              </div>
            </div>

            {/* Visual Level Comparison Bar */}
            <div style={{ background: '#F8FAFC', borderRadius: '12px', padding: '14px 18px', border: '1px solid #E2E8F0', marginBottom: '14px' }}>
              <div className="grid-2" style={{ gap: '16px' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                    <span style={{ color: '#64748B', fontWeight: 600 }}>Current Assessed Level:</span>
                    <strong style={{ color: getLevelColor(item.current_level) }}>{item.current_level}</strong>
                  </div>
                  <div style={{ height: '6px', background: '#E2E8F0', borderRadius: '9999px', overflow: 'hidden' }}>
                    <div style={{
                      height: '100%',
                      width: `${(item.current_val / 3.0) * 100}%`,
                      background: getLevelColor(item.current_level),
                      borderRadius: '9999px'
                    }} />
                  </div>
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                    <span style={{ color: '#64748B', fontWeight: 600 }}>Target Role Required Level:</span>
                    <strong style={{ color: '#312E81' }}>{item.required_level}</strong>
                  </div>
                  <div style={{ height: '6px', background: '#E2E8F0', borderRadius: '9999px', overflow: 'hidden' }}>
                    <div style={{
                      height: '100%',
                      width: `${(item.required_val / 3.0) * 100}%`,
                      background: '#4F46E5',
                      borderRadius: '9999px'
                    }} />
                  </div>
                </div>
              </div>
            </div>

            {/* Action to Bridge Gap */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}>
              <div style={{ fontSize: '13px', color: '#475569' }}>
                Recommended Topic to Bridge Gap: <strong style={{ color: '#4F46E5' }}>{item.recommended_topic}</strong>
              </div>

              {item.recommended_topic_id && (
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => {
                    setSelectedTopicId(item.recommended_topic_id);
                    setActiveTab('topics');
                  }}
                >
                  <BookOpen size={14} />
                  <span>Study Topic</span>
                  <ArrowRight size={14} />
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
