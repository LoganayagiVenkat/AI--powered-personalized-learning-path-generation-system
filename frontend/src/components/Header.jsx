import React from 'react';
import { Mic, Sparkles, BrainCircuit, Bell, Compass, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Header({ activeTab, onOpenVoice }) {
  const { user, profile, logout } = useAuth();

  const titles = {
    'dashboard': 'Student Learning Dashboard',
    'learning-path': 'AI Personalized Learning Path',
    'assessment': 'Diagnostic Skill Assessment',
    'skill-gap': 'Skill Gap Analysis & Career Mapping',
    'topics': 'Curriculum Topics & Study Materials',
    'chat': 'AI Conversational Tutor & Voice Assistant',
    'progress': 'Progress Tracking & Analytics',
    'recommendations': 'AI Recommendations Engine',
    'profile': 'Student Profile & Goals'
  };

  return (
    <header style={{
      height: '70px',
      background: '#FFFFFF',
      borderBottom: '1px solid #E2E8F0',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 36px',
      position: 'sticky',
      top: 0,
      zIndex: 40
    }}>
      {/* Page Title & Breadcrumb */}
      <div>
        <h1 style={{ fontSize: '18px', fontWeight: 800, color: '#0F172A', display: 'flex', alignItems: 'center', gap: '8px' }}>
          {titles[activeTab] || 'Dashboard'}
        </h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: '#64748B' }}>
          <span>PathGen Engine</span>
          <span>•</span>
          <span style={{ color: '#6366F1', fontWeight: 600 }}>Adaptive AI 2.0</span>
        </div>
      </div>

      {/* Header Actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {/* Career Goal Pill */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          background: 'var(--primary-light)',
          padding: '6px 14px',
          borderRadius: '9999px',
          border: '1px solid #E0E7FF'
        }}>
          <Compass size={15} color="#4F46E5" />
          <span style={{ fontSize: '12px', fontWeight: 700, color: '#4338CA' }}>
            Goal: {user?.target_job_role || 'Data Scientist'}
          </span>
        </div>

        {/* Quick Voice Assistant Trigger Button */}
        <button
          onClick={onOpenVoice}
          className="btn btn-sm"
          style={{
            background: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)',
            color: 'white',
            borderRadius: '9999px',
            padding: '7px 14px',
            boxShadow: '0 2px 8px rgba(99, 102, 241, 0.25)'
          }}
          title="Launch Voice Assistant"
        >
          <Mic size={15} />
          <span>Voice AI</span>
        </button>

        {/* User Pill */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          background: '#F8FAFC',
          border: '1px solid #E2E8F0',
          borderRadius: '9999px',
          padding: '4px 12px 4px 5px'
        }}>
          <div style={{
            width: '30px',
            height: '30px',
            borderRadius: '50%',
            background: 'var(--gradient-soft)',
            border: '2px solid #C7D2FE',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 700,
            color: '#4F46E5',
            fontSize: '13px'
          }}>
            {user?.name ? user.name.charAt(0) : 'S'}
          </div>
          <span style={{ fontSize: '13px', fontWeight: 700, color: '#1E293B' }}>
            {user?.name || 'Student'}
          </span>
        </div>

        {/* Header Sign Out Action */}
        <button
          onClick={logout}
          className="btn btn-secondary btn-sm"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            color: '#DC2626',
            borderColor: '#FEE2E2',
            background: '#FEF2F2',
            fontWeight: 600,
            cursor: 'pointer'
          }}
          title="Sign Out of Account"
        >
          <LogOut size={14} color="#DC2626" />
          <span>Sign Out</span>
        </button>
      </div>
    </header>
  );
}
