import React, { useState } from 'react';
import {
  Sparkles,
  Lock,
  Mail,
  User as UserIcon,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  Eye,
  EyeOff,
  ShieldCheck,
  Zap,
  TrendingUp,
  Award
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function AuthPage() {
  const { login, register } = useAuth();

  const [activeTab, setActiveTab] = useState('signin'); // 'signin' or 'signup'
  const [showPassword, setShowPassword] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [loading, setLoading] = useState(false);

  // Sign In form
  const [signInEmail, setSignInEmail] = useState('alex.morgan@example.com');
  const [signInPassword, setSignInPassword] = useState('password123');

  // Sign Up form
  const [signUpName, setSignUpName] = useState('');
  const [signUpEmail, setSignUpEmail] = useState('');
  const [signUpPassword, setSignUpPassword] = useState('');
  const [signUpRole, setSignUpRole] = useState('Data Scientist');
  const [signUpSkillLevel, setSignUpSkillLevel] = useState('Beginner');
  const [signUpEducation, setSignUpEducation] = useState('Undergraduate');
  const [signUpExperience, setSignUpExperience] = useState('Beginner');

  // Quick Demo Logins
  const demoAccounts = [
    {
      name: 'Alex Morgan',
      email: 'alex.morgan@example.com',
      role: 'Data Scientist',
      level: 'Beginner'
    },
    {
      name: 'Priya Sharma',
      email: 'priya.sharma@example.com',
      role: 'AI / ML Engineer',
      level: 'Intermediate'
    },
    {
      name: 'Marcus Chen',
      email: 'marcus.chen@example.com',
      role: 'Full Stack Developer',
      level: 'Advanced'
    },
    {
      name: 'Aisha Patel',
      email: 'aisha.patel@example.com',
      role: 'Data Scientist',
      level: 'Beginner'
    }
  ];

  const handleQuickFill = (acc) => {
    setActiveTab('signin');
    setSignInEmail(acc.email);
    setSignInPassword('password123');
    setErrorMsg('');
  };

  const handleSignInSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');

    if (!signInEmail || !signInPassword) {
      setErrorMsg('Please enter both email and password.');
      return;
    }

    try {
      setLoading(true);
      await login(signInEmail.trim().toLowerCase(), signInPassword);
      setSuccessMsg('Signed in successfully! Redirecting...');
    } catch (err) {
      setErrorMsg(err.message || 'Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSignUpSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');

    if (!signUpName || !signUpEmail || !signUpPassword) {
      setErrorMsg('Please fill in your name, email, and password.');
      return;
    }

    try {
      setLoading(true);
      await register({
        name: signUpName.trim(),
        email: signUpEmail.trim().toLowerCase(),
        password: signUpPassword,
        target_job_role: signUpRole,
        overall_skill_level: signUpSkillLevel,
        education_level: signUpEducation,
        experience_level: signUpExperience
      });
      setSuccessMsg('Account created successfully! Welcome to PathGen AI!');
    } catch (err) {
      setErrorMsg(err.message || 'Failed to create account. Email may already be in use.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      width: '100vw',
      background: 'linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '24px',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Decorative background glow circles */}
      <div style={{
        position: 'absolute',
        top: '-10%',
        left: '-5%',
        width: '500px',
        height: '500px',
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, transparent 70%)',
        pointerEvents: 'none'
      }} />
      <div style={{
        position: 'absolute',
        bottom: '-10%',
        right: '-5%',
        width: '600px',
        height: '600px',
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(168, 85, 247, 0.2) 0%, transparent 70%)',
        pointerEvents: 'none'
      }} />

      {/* Main Container Card */}
      <div style={{
        maxWidth: '1080px',
        width: '100%',
        background: 'rgba(255, 255, 255, 0.98)',
        borderRadius: '24px',
        boxShadow: '0 25px 60px -15px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.1)',
        display: 'grid',
        gridTemplateColumns: '1.05fr 1fr',
        overflow: 'hidden',
        position: 'relative',
        zIndex: 10
      }}>
        {/* Left Hero Brand Panel */}
        <div style={{
          background: 'linear-gradient(145deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%)',
          padding: '48px 40px',
          color: 'white',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}>
          <div>
            {/* Brand Logo */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '32px' }}>
              <div style={{
                width: '46px',
                height: '46px',
                borderRadius: '14px',
                background: 'linear-gradient(135deg, #6366F1 0%, #A855F7 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 8px 20px rgba(99, 102, 241, 0.4)'
              }}>
                <Sparkles size={24} color="white" />
              </div>
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 800, letterSpacing: '-0.02em', margin: 0 }}>
                  PathGen AI
                </h2>
                <span style={{ fontSize: '11px', color: '#C7D2FE', fontWeight: 600, letterSpacing: '0.06em', textTransform: 'uppercase' }}>
                  Personalized Learning Engine
                </span>
              </div>
            </div>

            {/* Headline */}
            <h1 style={{ fontSize: '28px', fontWeight: 800, lineHeight: 1.25, marginBottom: '14px', letterSpacing: '-0.02em' }}>
              Master Your Dream Career with AI Guidance
            </h1>
            <p style={{ fontSize: '14px', color: '#E0E7FF', lineHeight: 1.6, marginBottom: '32px' }}>
              Sign in to access your custom DAG topological learning path, adaptive quizzes, skill gap radar, and AI voice tutor.
            </p>

            {/* Feature Highlights */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '10px',
                  background: 'rgba(255, 255, 255, 0.12)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Zap size={18} color="#FBBF24" />
                </div>
                <div>
                  <div style={{ fontSize: '13.5px', fontWeight: 700 }}>Topological Prerequisite Ordering</div>
                  <div style={{ fontSize: '12px', color: '#C7D2FE' }}>Zero confusion — learn every foundational topic in order</div>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '10px',
                  background: 'rgba(255, 255, 255, 0.12)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <TrendingUp size={18} color="#34D399" />
                </div>
                <div>
                  <div style={{ fontSize: '13.5px', fontWeight: 700 }}>Continuous Skill-Gap Matrix</div>
                  <div style={{ fontSize: '12px', color: '#C7D2FE' }}>Mathematical vector comparison against industry roles</div>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '10px',
                  background: 'rgba(255, 255, 255, 0.12)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Award size={18} color="#60A5FA" />
                </div>
                <div>
                  <div style={{ fontSize: '13.5px', fontWeight: 700 }}>Dynamic Adaptive Quizzes & Voice AI</div>
                  <div style={{ fontSize: '12px', color: '#C7D2FE' }}>Real-time speech tutoring & flashcard practice</div>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Demo Fill Box */}
          <div style={{
            marginTop: '36px',
            background: 'rgba(255, 255, 255, 0.08)',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            borderRadius: '14px',
            padding: '16px'
          }}>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#F8FAFC', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <ShieldCheck size={14} color="#818CF8" />
              <span>One-Click Demo Student Sign-In:</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
              {demoAccounts.map((acc) => (
                <button
                  key={acc.email}
                  type="button"
                  onClick={() => handleQuickFill(acc)}
                  style={{
                    background: signInEmail === acc.email ? 'rgba(99, 102, 241, 0.45)' : 'rgba(255, 255, 255, 0.07)',
                    border: signInEmail === acc.email ? '1px solid #818CF8' : '1px solid rgba(255, 255, 255, 0.12)',
                    borderRadius: '8px',
                    padding: '8px 10px',
                    textAlign: 'left',
                    color: 'white',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.18)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = signInEmail === acc.email ? 'rgba(99, 102, 241, 0.45)' : 'rgba(255, 255, 255, 0.07)';
                  }}
                >
                  <div style={{ fontSize: '12px', fontWeight: 700 }}>{acc.name}</div>
                  <div style={{ fontSize: '10px', color: '#C7D2FE' }}>{acc.role}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Auth Form Panel */}
        <div style={{
          padding: '48px 40px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center'
        }}>
          {/* Tabs */}
          <div style={{
            display: 'flex',
            background: '#F1F5F9',
            padding: '4px',
            borderRadius: '12px',
            marginBottom: '28px'
          }}>
            <button
              type="button"
              onClick={() => { setActiveTab('signin'); setErrorMsg(''); setSuccessMsg(''); }}
              style={{
                flex: 1,
                padding: '10px 16px',
                borderRadius: '8px',
                border: 'none',
                background: activeTab === 'signin' ? '#FFFFFF' : 'transparent',
                color: activeTab === 'signin' ? '#0F172A' : '#64748B',
                fontWeight: activeTab === 'signin' ? 700 : 600,
                fontSize: '14px',
                cursor: 'pointer',
                boxShadow: activeTab === 'signin' ? '0 2px 6px rgba(0,0,0,0.08)' : 'none',
                transition: 'all 0.15s ease'
              }}
            >
              Sign In
            </button>
            <button
              type="button"
              onClick={() => { setActiveTab('signup'); setErrorMsg(''); setSuccessMsg(''); }}
              style={{
                flex: 1,
                padding: '10px 16px',
                borderRadius: '8px',
                border: 'none',
                background: activeTab === 'signup' ? '#FFFFFF' : 'transparent',
                color: activeTab === 'signup' ? '#0F172A' : '#64748B',
                fontWeight: activeTab === 'signup' ? 700 : 600,
                fontSize: '14px',
                cursor: 'pointer',
                boxShadow: activeTab === 'signup' ? '0 2px 6px rgba(0,0,0,0.08)' : 'none',
                transition: 'all 0.15s ease'
              }}
            >
              Create Account
            </button>
          </div>

          {/* Form Header */}
          <div style={{ marginBottom: '24px' }}>
            <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#0F172A', margin: '0 0 6px' }}>
              {activeTab === 'signin' ? 'Welcome Back' : 'Start Your Journey'}
            </h2>
            <p style={{ fontSize: '13.5px', color: '#64748B', margin: 0 }}>
              {activeTab === 'signin'
                ? 'Enter your credentials to continue your learning roadmap.'
                : 'Create your personalized student profile in seconds.'}
            </p>
          </div>

          {/* Alert Banners */}
          {errorMsg && (
            <div style={{
              padding: '12px 14px',
              borderRadius: '10px',
              background: '#FEF2F2',
              border: '1px solid #FECACA',
              color: '#DC2626',
              fontSize: '13px',
              marginBottom: '18px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <AlertCircle size={16} flexShrink={0} />
              <span>{errorMsg}</span>
            </div>
          )}

          {successMsg && (
            <div style={{
              padding: '12px 14px',
              borderRadius: '10px',
              background: '#F0FDF4',
              border: '1px solid #BBF7D0',
              color: '#16A34A',
              fontSize: '13px',
              marginBottom: '18px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <CheckCircle2 size={16} flexShrink={0} />
              <span>{successMsg}</span>
            </div>
          )}

          {/* SIGN IN FORM */}
          {activeTab === 'signin' && (
            <form onSubmit={handleSignInSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>
                  Email Address
                </label>
                <div style={{ position: 'relative' }}>
                  <Mail size={17} color="#94A3B8" style={{ position: 'absolute', left: '14px', top: '14px' }} />
                  <input
                    type="email"
                    value={signInEmail}
                    onChange={(e) => setSignInEmail(e.target.value)}
                    placeholder="student@example.com"
                    style={{
                      width: '100%',
                      padding: '12px 14px 12px 42px',
                      borderRadius: '10px',
                      border: '1.5px solid #CBD5E1',
                      fontSize: '14px',
                      outline: 'none',
                      transition: 'border-color 0.15s ease'
                    }}
                    onFocus={(e) => e.target.style.borderColor = '#6366F1'}
                    onBlur={(e) => e.target.style.borderColor = '#CBD5E1'}
                    required
                  />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <label style={{ fontSize: '13px', fontWeight: 600, color: '#334155' }}>
                    Password
                  </label>
                  <span style={{ fontSize: '12px', color: '#6366F1', fontWeight: 600 }}>
                    Default: <code>password123</code>
                  </span>
                </div>
                <div style={{ position: 'relative' }}>
                  <Lock size={17} color="#94A3B8" style={{ position: 'absolute', left: '14px', top: '14px' }} />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={signInPassword}
                    onChange={(e) => setSignInPassword(e.target.value)}
                    placeholder="Enter your password"
                    style={{
                      width: '100%',
                      padding: '12px 42px 12px 42px',
                      borderRadius: '10px',
                      border: '1.5px solid #CBD5E1',
                      fontSize: '14px',
                      outline: 'none',
                      transition: 'border-color 0.15s ease'
                    }}
                    onFocus={(e) => e.target.style.borderColor = '#6366F1'}
                    onBlur={(e) => e.target.style.borderColor = '#CBD5E1'}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: 'absolute',
                      right: '12px',
                      top: '12px',
                      background: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      color: '#94A3B8'
                    }}
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary"
                style={{
                  padding: '13px',
                  borderRadius: '10px',
                  fontSize: '15px',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  marginTop: '6px',
                  boxShadow: '0 4px 14px rgba(99, 102, 241, 0.35)'
                }}
              >
                {loading ? 'Authenticating...' : 'Sign In to PathGen AI'}
                {!loading && <ArrowRight size={18} />}
              </button>
            </form>
          )}

          {/* SIGN UP FORM */}
          {activeTab === 'signup' && (
            <form onSubmit={handleSignUpSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '12.5px', fontWeight: 600, color: '#334155', marginBottom: '4px' }}>
                  Full Name *
                </label>
                <div style={{ position: 'relative' }}>
                  <UserIcon size={16} color="#94A3B8" style={{ position: 'absolute', left: '12px', top: '12px' }} />
                  <input
                    type="text"
                    value={signUpName}
                    onChange={(e) => setSignUpName(e.target.value)}
                    placeholder="e.g. Ramesh Kumar"
                    style={{
                      width: '100%',
                      padding: '10px 12px 10px 36px',
                      borderRadius: '8px',
                      border: '1.5px solid #CBD5E1',
                      fontSize: '13.5px'
                    }}
                    required
                  />
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '12.5px', fontWeight: 600, color: '#334155', marginBottom: '4px' }}>
                  Email Address *
                </label>
                <div style={{ position: 'relative' }}>
                  <Mail size={16} color="#94A3B8" style={{ position: 'absolute', left: '12px', top: '12px' }} />
                  <input
                    type="email"
                    value={signUpEmail}
                    onChange={(e) => setSignUpEmail(e.target.value)}
                    placeholder="ramesh@example.com"
                    style={{
                      width: '100%',
                      padding: '10px 12px 10px 36px',
                      borderRadius: '8px',
                      border: '1.5px solid #CBD5E1',
                      fontSize: '13.5px'
                    }}
                    required
                  />
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '12.5px', fontWeight: 600, color: '#334155', marginBottom: '4px' }}>
                  Password *
                </label>
                <div style={{ position: 'relative' }}>
                  <Lock size={16} color="#94A3B8" style={{ position: 'absolute', left: '12px', top: '12px' }} />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={signUpPassword}
                    onChange={(e) => setSignUpPassword(e.target.value)}
                    placeholder="Create a password"
                    style={{
                      width: '100%',
                      padding: '10px 36px 10px 36px',
                      borderRadius: '8px',
                      border: '1.5px solid #CBD5E1',
                      fontSize: '13.5px'
                    }}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: 'absolute',
                      right: '10px',
                      top: '10px',
                      background: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      color: '#94A3B8'
                    }}
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#334155', marginBottom: '4px' }}>
                    Target Job Role *
                  </label>
                  <select
                    value={signUpRole}
                    onChange={(e) => setSignUpRole(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '8px 10px',
                      borderRadius: '8px',
                      border: '1.5px solid #CBD5E1',
                      fontSize: '13px',
                      background: 'white'
                    }}
                  >
                    <option value="Data Scientist">Data Scientist</option>
                    <option value="AI / ML Engineer">AI / ML Engineer</option>
                    <option value="Full Stack Developer">Full Stack Developer</option>
                  </select>
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#334155', marginBottom: '4px' }}>
                    Initial Skill Level
                  </label>
                  <select
                    value={signUpSkillLevel}
                    onChange={(e) => setSignUpSkillLevel(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '8px 10px',
                      borderRadius: '8px',
                      border: '1.5px solid #CBD5E1',
                      fontSize: '13px',
                      background: 'white'
                    }}
                  >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#334155', marginBottom: '4px' }}>
                    Education Level
                  </label>
                  <select
                    value={signUpEducation}
                    onChange={(e) => setSignUpEducation(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '8px 10px',
                      borderRadius: '8px',
                      border: '1.5px solid #CBD5E1',
                      fontSize: '13px',
                      background: 'white'
                    }}
                  >
                    <option value="Undergraduate">Undergraduate</option>
                    <option value="Graduate">Graduate</option>
                    <option value="Self-Taught">Self-Taught</option>
                    <option value="Working Professional">Working Professional</option>
                  </select>
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#334155', marginBottom: '4px' }}>
                    Experience
                  </label>
                  <select
                    value={signUpExperience}
                    onChange={(e) => setSignUpExperience(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '8px 10px',
                      borderRadius: '8px',
                      border: '1.5px solid #CBD5E1',
                      fontSize: '13px',
                      background: 'white'
                    }}
                  >
                    <option value="Beginner">Beginner (0-1 yrs)</option>
                    <option value="Intermediate">Intermediate (1-3 yrs)</option>
                    <option value="Advanced">Advanced (3+ yrs)</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary"
                style={{
                  padding: '12px',
                  borderRadius: '10px',
                  fontSize: '14.5px',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  marginTop: '6px',
                  boxShadow: '0 4px 14px rgba(99, 102, 241, 0.35)'
                }}
              >
                {loading ? 'Registering...' : 'Create Account & Start Learning'}
                {!loading && <ArrowRight size={16} />}
              </button>
            </form>
          )}

          {/* Switch Tab Prompt */}
          <div style={{ textAlign: 'center', marginTop: '20px', fontSize: '13px', color: '#64748B' }}>
            {activeTab === 'signin' ? (
              <span>
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={() => { setActiveTab('signup'); setErrorMsg(''); }}
                  style={{ background: 'transparent', border: 'none', color: '#6366F1', fontWeight: 700, cursor: 'pointer' }}
                >
                  Create one now
                </button>
              </span>
            ) : (
              <span>
                Already registered?{' '}
                <button
                  type="button"
                  onClick={() => { setActiveTab('signin'); setErrorMsg(''); }}
                  style={{ background: 'transparent', border: 'none', color: '#6366F1', fontWeight: 700, cursor: 'pointer' }}
                >
                  Sign in here
                </button>
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
