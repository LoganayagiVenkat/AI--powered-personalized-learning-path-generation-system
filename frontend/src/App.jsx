import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import FloatingVoiceModal from './components/FloatingVoiceModal';

import DashboardPage from './pages/DashboardPage';
import LearningPathPage from './pages/LearningPathPage';
import SkillAssessmentPage from './pages/SkillAssessmentPage';
import SkillGapPage from './pages/SkillGapPage';
import TopicsListPage from './pages/TopicsListPage';
import TopicLearningPage from './pages/TopicLearningPage';
import QuizPage from './pages/QuizPage';
import ProgressTrackingPage from './pages/ProgressTrackingPage';
import ChatbotPage from './pages/ChatbotPage';
import RecommendationsPage from './pages/RecommendationsPage';
import ProfilePage from './pages/ProfilePage';
import AuthPage from './pages/AuthPage';
import { Mic, Sparkles } from 'lucide-react';

function MainApp() {
  const { user, loading } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedTopicId, setSelectedTopicId] = useState(null);
  const [isVoiceOpen, setIsVoiceOpen] = useState(false);

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#0F172A',
        color: 'white',
        flexDirection: 'column',
        gap: '16px'
      }}>
        <div style={{
          width: '50px',
          height: '50px',
          borderRadius: '16px',
          background: 'linear-gradient(135deg, #6366F1 0%, #A855F7 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 8px 24px rgba(99, 102, 241, 0.45)'
        }}>
          <Sparkles size={26} color="white" />
        </div>
        <p style={{ fontSize: '15px', fontWeight: 600, color: '#C7D2FE', letterSpacing: '-0.01em' }}>
          Initializing PathGen AI Learning System...
        </p>
      </div>
    );
  }

  if (!user) {
    return <AuthPage />;
  }

  const renderActivePage = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardPage setActiveTab={setActiveTab} setSelectedTopicId={setSelectedTopicId} />;
      case 'learning-path':
        return <LearningPathPage setActiveTab={setActiveTab} setSelectedTopicId={setSelectedTopicId} />;
      case 'assessment':
        return <SkillAssessmentPage setActiveTab={setActiveTab} />;
      case 'skill-gap':
        return <SkillGapPage setActiveTab={setActiveTab} setSelectedTopicId={setSelectedTopicId} />;
      case 'topics':
        if (selectedTopicId) {
          return (
            <div>
              <div style={{ padding: '0 36px 14px', maxWidth: '1400px', margin: '0 auto' }}>
                <button
                  onClick={() => setSelectedTopicId(null)}
                  className="btn btn-secondary btn-sm"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}
                >
                  ← Back to All Curriculum Topics
                </button>
              </div>
              <TopicLearningPage
                topicId={selectedTopicId}
                setActiveTab={setActiveTab}
                setSelectedTopicId={setSelectedTopicId}
              />
            </div>
          );
        }
        return <TopicsListPage setActiveTab={setActiveTab} setSelectedTopicId={setSelectedTopicId} />;
      case 'quiz':
        return (
          <QuizPage
            topicId={selectedTopicId || 1}
            setActiveTab={setActiveTab}
            setSelectedTopicId={setSelectedTopicId}
          />
        );
      case 'chat':
        return <ChatbotPage onOpenVoice={() => setIsVoiceOpen(true)} />;
      case 'progress':
        return <ProgressTrackingPage setActiveTab={setActiveTab} setSelectedTopicId={setSelectedTopicId} />;
      case 'recommendations':
        return <RecommendationsPage setActiveTab={setActiveTab} setSelectedTopicId={setSelectedTopicId} />;
      case 'profile':
        return <ProfilePage setActiveTab={setActiveTab} />;
      default:
        return <DashboardPage setActiveTab={setActiveTab} setSelectedTopicId={setSelectedTopicId} />;
    }
  };

  return (
    <div className="app-container">
      {/* Sleek Modern Navigation Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main App Content Viewport */}
      <div className="main-content">
        <Header activeTab={activeTab} onOpenVoice={() => setIsVoiceOpen(true)} />
        <main key={user?.id || 1}>{renderActivePage()}</main>
      </div>

      {/* Global Floating Voice Assistant Trigger */}
      <button
        onClick={() => setIsVoiceOpen(true)}
        className="floating-mic-btn"
        title="Open Voice Assistant"
      >
        <Mic size={26} />
      </button>

      {/* Voice Assistant Interactive Modal */}
      <FloatingVoiceModal
        isOpen={isVoiceOpen}
        onClose={() => setIsVoiceOpen(false)}
      />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
}
