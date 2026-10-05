import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  Search,
  Clock,
  Sparkles,
  ArrowRight,
  Filter
} from 'lucide-react';
import api from '../services/api';

export default function TopicsListPage({ setActiveTab, setSelectedTopicId }) {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All');

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        setLoading(true);
        const data = await api.getTopics();
        setTopics(data);
      } catch (err) {
        console.error('Error fetching topics:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchTopics();
  }, []);

  const categories = ['All', 'Programming', 'Mathematics', 'Data', 'AI/ML'];

  const filtered = topics.filter(t => {
    const matchesCat = categoryFilter === 'All' || t.category === categoryFilter;
    const matchesSearch = t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          t.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesSearch;
  });

  if (loading) {
    return (
      <div className="page-wrapper" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <Sparkles size={36} color="#6366F1" style={{ animation: 'spin 2s linear infinite' }} />
          <p style={{ marginTop: '12px', fontWeight: 600, color: '#64748B' }}>Loading complete curriculum database...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-wrapper">
      {/* Top Banner */}
      <div className="card-gradient-border" style={{ marginBottom: '28px' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'var(--primary-light)', padding: '4px 12px', borderRadius: '9999px', fontSize: '12px', fontWeight: 700, color: '#4F46E5', marginBottom: '8px' }}>
          <BookOpen size={14} /> Full Curriculum Library
        </div>
        <h1 style={{ fontSize: '24px', fontWeight: 800, color: '#0F172A' }}>
          Curriculum Topics & Learning Modules
        </h1>
        <p style={{ fontSize: '14px', color: '#64748B', marginTop: '4px' }}>
          Explore foundational and advanced technical modules designed for modern AI and software engineering careers.
        </p>

        {/* Search and Filters */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginTop: '20px', paddingTop: '16px', borderTop: '1px solid #E2E8F0' }}>
          {/* Search Bar */}
          <div style={{ position: 'relative', width: '320px' }}>
            <Search size={16} color="#94A3B8" style={{ position: 'absolute', left: '12px', top: '13px' }} />
            <input
              type="text"
              placeholder="Search topics, keywords, concepts..."
              className="form-input"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ paddingLeft: '38px', borderRadius: '9999px' }}
            />
          </div>

          {/* Category Chips */}
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setCategoryFilter(cat)}
                style={{
                  padding: '6px 14px',
                  borderRadius: '9999px',
                  border: 'none',
                  background: categoryFilter === cat ? 'var(--primary)' : '#E2E8F0',
                  color: categoryFilter === cat ? 'white' : '#475569',
                  fontSize: '12px',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Topics Grid */}
      <div className="grid-2">
        {filtered.map((topic) => (
          <div key={topic.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="badge badge-purple">{topic.category}</span>
                  <span className="badge badge-blue">{topic.difficulty}</span>
                </div>
                <span style={{ fontSize: '12px', color: '#64748B', display: 'flex', alignItems: 'center', gap: '4px' }}>
                  <Clock size={13} /> {topic.estimated_hours} Hours
                </span>
              </div>

              <h3 style={{ fontSize: '17px', fontWeight: 800, color: '#0F172A', marginBottom: '8px' }}>
                {topic.title}
              </h3>

              <p style={{ fontSize: '13.5px', color: '#475569', lineHeight: 1.6, marginBottom: '14px' }}>
                {topic.description}
              </p>

              {/* Concepts Tags */}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '16px' }}>
                {topic.concepts?.slice(0, 4).map((c, idx) => (
                  <span key={idx} style={{
                    fontSize: '11px',
                    background: '#F1F5F9',
                    color: '#475569',
                    padding: '3px 8px',
                    borderRadius: '6px',
                    fontWeight: 500
                  }}>
                    {c}
                  </span>
                ))}
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingTop: '14px', borderTop: '1px solid #F1F5F9' }}>
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => {
                  setSelectedTopicId(topic.id);
                  setActiveTab('quiz');
                }}
              >
                Topic Quiz
              </button>

              <button
                className="btn btn-primary btn-sm"
                onClick={() => {
                  setSelectedTopicId(topic.id);
                  setActiveTab('topics');
                }}
              >
                <span>Study Lesson</span>
                <ArrowRight size={14} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
