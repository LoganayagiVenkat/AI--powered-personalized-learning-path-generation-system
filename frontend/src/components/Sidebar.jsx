import React from 'react';
import {
  LayoutDashboard,
  MapPin,
  ClipboardCheck,
  Split,
  BookOpen,
  MessageSquare,
  BarChart3,
  Sparkles,
  User,
  Flame,
  Award,
  LogOut
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Sidebar({ activeTab, setActiveTab }) {
  const { user, profile, logout } = useAuth();

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'learning-path', label: 'AI Learning Path', icon: MapPin, badge: 'AI' },
    { id: 'assessment', label: 'Skill Assessment', icon: ClipboardCheck },
    { id: 'skill-gap', label: 'Skill Gap Analysis', icon: Split },
    { id: 'topics', label: 'Curriculum & Study', icon: BookOpen },
    { id: 'quiz', label: 'AI Quiz & Flashcards', icon: Award, badge: 'New' },
    { id: 'chat', label: 'AI Tutor & Voice', icon: MessageSquare, badge: 'Live' },
    { id: 'progress', label: 'Progress Tracking', icon: BarChart3 },
    { id: 'recommendations', label: 'Recommendations', icon: Sparkles },
    { id: 'profile', label: 'Student Profile', icon: User },
  ];

  return (
    <aside style={{
      width: '270px',
      background: '#FFFFFF',
      borderRight: '1px solid #E2E8F0',
      display: 'flex',
      flexDirection: 'column',
      padding: '24px 16px',
      height: '100vh',
      position: 'sticky',
      top: 0,
      zIndex: 50,
      flexShrink: 0
    }}>
      {/* Brand Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '0 8px 24px', borderBottom: '1px solid #F1F5F9' }}>
        <div style={{
          width: '42px',
          height: '42px',
          borderRadius: '12px',
          background: 'var(--gradient-brand)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          boxShadow: '0 4px 12px rgba(99, 102, 241, 0.35)'
        }}>
          <Sparkles size={22} />
        </div>
        <div>
          <h2 style={{ fontSize: '16px', fontWeight: 800, color: '#0F172A', lineHeight: 1.2 }}>PathGen AI</h2>
          <span style={{ fontSize: '11px', color: '#6366F1', fontWeight: 700, letterSpacing: '0.04em', textTransform: 'uppercase' }}>Adaptive Learning</span>
        </div>
      </div>

      {/* Student Mini Card */}
      <div
        style={{
          margin: '16px 4px',
          padding: '12px 14px',
          borderRadius: '12px',
          background: '#F8FAFC',
          border: '1px solid #E2E8F0'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
          <span style={{ fontSize: '12.5px', fontWeight: 700, color: '#1E293B' }}>{user?.name || 'Student'}</span>
          <span className="badge badge-purple" style={{ fontSize: '10px', padding: '2px 6px' }}>
            {profile?.overall_skill_level || 'Beginner'}
          </span>
        </div>
        <div style={{ fontSize: '11px', color: '#64748B', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          Target: <strong style={{ color: '#4F46E5' }}>{user?.target_job_role || 'Data Scientist'}</strong>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '8px', paddingTop: '8px', borderTop: '1px solid #E2E8F0' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: '#EA580C', fontWeight: 600 }}>
            <Flame size={14} /> {profile?.streak_days || 1}d Streak
          </div>
          <div style={{ fontSize: '10.5px', color: '#059669', fontWeight: 700 }}>
            ● Active
          </div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '4px', overflowY: 'auto', paddingRight: '4px' }}>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '10px 14px',
                borderRadius: '10px',
                border: 'none',
                background: isActive ? 'var(--primary-light)' : 'transparent',
                color: isActive ? 'var(--primary)' : '#475569',
                fontFamily: 'inherit',
                fontSize: '13.5px',
                fontWeight: isActive ? 700 : 500,
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                textAlign: 'left'
              }}
              onMouseEnter={(e) => {
                if (!isActive) e.currentTarget.style.background = '#F8FAFC';
              }}
              onMouseLeave={(e) => {
                if (!isActive) e.currentTarget.style.background = 'transparent';
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <Icon size={18} color={isActive ? '#4F46E5' : '#64748B'} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span style={{
                  fontSize: '10px',
                  fontWeight: 700,
                  padding: '2px 6px',
                  borderRadius: '6px',
                  background: isActive ? '#6366F1' : '#E2E8F0',
                  color: isActive ? 'white' : '#475569'
                }}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Sign Out Button */}
      <div style={{ borderTop: '1px solid #F1F5F9', paddingTop: '14px', marginTop: '10px' }}>
        <button
          onClick={logout}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            width: '100%',
            padding: '9px 14px',
            borderRadius: '10px',
            border: '1px solid #FEE2E2',
            background: '#FEF2F2',
            color: '#DC2626',
            fontSize: '13px',
            fontWeight: 700,
            cursor: 'pointer',
            transition: 'all 0.15s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#FEE2E2';
            e.currentTarget.style.borderColor = '#FCA5A5';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = '#FEF2F2';
            e.currentTarget.style.borderColor = '#FEE2E2';
          }}
          title="Sign out of PathGen AI"
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <LogOut size={16} color="#DC2626" />
            <span>Sign Out</span>
          </div>
          <span style={{ fontSize: '11px', color: '#991B1B', fontWeight: 600 }}>
            {user?.name?.split(' ')[0] || 'User'}
          </span>
        </button>
      </div>
    </aside>
  );
}
