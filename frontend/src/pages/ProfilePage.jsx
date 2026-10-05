import React, { useState, useEffect } from 'react';
import {
  User,
  Save,
  CheckCircle2,
  Sparkles,
  Compass,
  GraduationCap,
  Briefcase,
  Brain
} from 'lucide-react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function ProfilePage({ setActiveTab }) {
  const { user, profile, refreshProfile } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    education_level: 'Undergraduate',
    experience_level: 'Beginner',
    interests: 'Machine Learning, Data Science, Python, Deep Learning',
    target_job_role: 'Data Scientist',
    career_goal_id: 1,
    bio: ''
  });
  const [careerGoals, setCareerGoals] = useState([]);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    const loadProfileData = async () => {
      try {
        const [profData, goalsData] = await Promise.all([
          api.getProfile(),
          api.getCareerGoals()
        ]);
        setCareerGoals(goalsData || []);
        if (profData) {
          setFormData({
            name: profData.name || '',
            education_level: profData.education_level || 'Undergraduate',
            experience_level: profData.experience_level || 'Beginner',
            interests: profData.interests || 'Machine Learning, Data Science, Python',
            target_job_role: profData.target_job_role || 'Data Scientist',
            career_goal_id: profData.career_goal?.id || 1,
            bio: profData.bio || ''
          });
        }
      } catch (err) {
        console.error('Error loading profile data:', err);
      }
    };
    loadProfileData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCareerGoalSelect = (goalId) => {
    const matched = careerGoals.find(g => g.id === Number(goalId));
    setFormData(prev => ({
      ...prev,
      career_goal_id: Number(goalId),
      target_job_role: matched ? matched.target_role : prev.target_job_role
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      await api.updateProfile(formData);
      await api.generateLearningPath(); // Re-generate roadmap based on updated profile!
      await refreshProfile();
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      console.error('Error updating profile:', err);
      alert('Failed to update profile: ' + err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="page-wrapper" style={{ maxWidth: '900px', margin: '0 auto' }}>
      <div className="card-gradient-border" style={{ marginBottom: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            background: 'var(--gradient-brand)',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '22px',
            fontWeight: 800
          }}>
            {formData.name ? formData.name.charAt(0) : 'A'}
          </div>
          <div>
            <h1 style={{ fontSize: '22px', fontWeight: 800, color: '#0F172A' }}>
              Student Profile & Career Ambitions
            </h1>
            <p style={{ fontSize: '13px', color: '#64748B' }}>
              Updates to your education, interests, or career goal will dynamically re-generate your AI roadmap.
            </p>
          </div>
        </div>
      </div>

      {saveSuccess && (
        <div style={{
          background: '#ECFDF5',
          border: '1px solid #A7F3D0',
          color: '#065F46',
          borderRadius: '12px',
          padding: '14px 18px',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          fontSize: '14px',
          fontWeight: 600
        }}>
          <CheckCircle2 size={18} color="#059669" />
          <span>Profile saved successfully! AI learning path has been re-calibrated.</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="card" style={{ padding: '32px' }}>
        {/* Name & Target Role */}
        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input
              type="text"
              name="name"
              className="form-input"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Target Job Role</label>
            <input
              type="text"
              name="target_job_role"
              className="form-input"
              value={formData.target_job_role}
              onChange={handleChange}
              placeholder="e.g. Data Scientist, AI Engineer"
              required
            />
          </div>
        </div>

        {/* Career Goal Track */}
        <div className="form-group">
          <label className="form-label">Target Career Track</label>
          <select
            name="career_goal_id"
            className="form-select"
            value={formData.career_goal_id}
            onChange={(e) => handleCareerGoalSelect(e.target.value)}
          >
            {careerGoals.map((g) => (
              <option key={g.id} value={g.id}>
                {g.title} ({g.target_role})
              </option>
            ))}
          </select>
        </div>

        {/* Education & Experience Level */}
        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Education Level</label>
            <select
              name="education_level"
              className="form-select"
              value={formData.education_level}
              onChange={handleChange}
            >
              <option value="High School">High School</option>
              <option value="Undergraduate">Undergraduate Degree</option>
              <option value="Graduate">Graduate (Master's / Ph.D.)</option>
              <option value="Working Professional">Working Professional / Career Transitioner</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Current Experience Level</label>
            <select
              name="experience_level"
              className="form-select"
              value={formData.experience_level}
              onChange={handleChange}
            >
              <option value="Beginner">Beginner (Starting fresh)</option>
              <option value="Intermediate">Intermediate (Some programming/math experience)</option>
              <option value="Advanced">Advanced (Experienced practitioner)</option>
            </select>
          </div>
        </div>

        {/* Free-form Interests for NLP TF-IDF extraction */}
        <div className="form-group">
          <label className="form-label">
            Interests & Focus Areas <span style={{ fontSize: '11px', color: '#6366F1' }}>(NLP Keyword Extracted)</span>
          </label>
          <input
            type="text"
            name="interests"
            className="form-input"
            value={formData.interests}
            onChange={handleChange}
            placeholder="e.g. Machine Learning, Neural Networks, Computer Vision, Transformers, SQL"
          />
          <span style={{ fontSize: '11px', color: '#64748B', display: 'block', marginTop: '4px' }}>
            Our NLP engine parses these tokens to calculate cosine similarity with topic curriculum definitions.
          </span>
        </div>

        {/* Student Bio */}
        <div className="form-group">
          <label className="form-label">Student Bio & Learning Objective</label>
          <textarea
            name="bio"
            rows={3}
            className="form-textarea"
            value={formData.bio}
            onChange={handleChange}
            placeholder="Share your goals, preferred pace, or background..."
          />
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '14px', marginTop: '24px', paddingTop: '20px', borderTop: '1px solid #E2E8F0' }}>
          <button
            type="button"
            onClick={() => setActiveTab('dashboard')}
            className="btn btn-secondary"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="btn btn-primary"
          >
            <Save size={16} />
            <span>{saving ? 'Saving & Generating Roadmap...' : 'Save Profile & Recalibrate Roadmap'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
