const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.userId = localStorage.getItem('user_id') || '1';
  }

  setUserId(id) {
    this.userId = String(id);
    localStorage.setItem('user_id', String(id));
  }

  clearAuth() {
    this.userId = null;
    localStorage.removeItem('user_id');
    localStorage.removeItem('token');
  }

  getHeaders(isFormData = false) {
    const headers = {
      'X-User-Id': this.userId
    };
    if (!isFormData) {
      headers['Content-Type'] = 'application/json';
    }
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
      ...this.getHeaders(options.body instanceof FormData),
      ...(options.headers || {})
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers
      });

      if (!response.ok) {
        let errMessage = `HTTP Error ${response.status}`;
        try {
          const errData = await response.json();
          errMessage = errData.error || errData.message || errMessage;
        } catch (_) {}
        throw new Error(errMessage);
      }

      return await response.json();
    } catch (err) {
      console.error(`API Error on [${options.method || 'GET'}] ${endpoint}:`, err);
      throw err;
    }
  }

  // Auth APIs
  login(email, password) {
    return this.request('/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
  }

  register(userData) {
    return this.request('/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  }

  getDemoAccounts() {
    return this.request('/auth/demo-accounts');
  }

  switchAccount(identifier) {
    const payload = typeof identifier === 'number' || !isNaN(Number(identifier))
      ? { user_id: Number(identifier) }
      : { email: identifier };
    return this.request('/auth/switch', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  }

  // Profile & Goals
  getProfile() {
    return this.request('/profile');
  }

  updateProfile(profileData) {
    return this.request('/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData)
    });
  }

  getCareerGoals() {
    return this.request('/career-goals');
  }

  getSkills() {
    return this.request('/skills');
  }

  // Skill Assessment
  getAssessment() {
    return this.request('/assessment');
  }

  submitAssessment(answers) {
    return this.request('/assessment', {
      method: 'POST',
      body: JSON.stringify({ answers })
    });
  }

  // Learning Path
  getLearningPath() {
    return this.request('/learning-path');
  }

  generateLearningPath() {
    return this.request('/learning-path/generate', {
      method: 'POST'
    });
  }

  getTopics() {
    return this.request('/topics');
  }

  getTopicDetail(topicId) {
    return this.request(`/topics/${topicId}`);
  }

  // Quizzes
  getTopicQuiz(topicId) {
    return this.request(`/quiz/${topicId}`);
  }

  submitQuiz(quizId, topicId, answers) {
    return this.request('/quiz', {
      method: 'POST',
      body: JSON.stringify({ quiz_id: quizId, topic_id: topicId, answers })
    });
  }

  generateDynamicQuiz(topicId, options = {}) {
    return this.request('/quiz/generate', {
      method: 'POST',
      body: JSON.stringify({
        topic_id: topicId,
        num_questions: options.num_questions || 5,
        difficulty: options.difficulty || 'Intermediate',
        focus_type: options.focus_type || 'conceptual',
        api_key: options.api_key
      })
    });
  }

  generateFlashcards(topicId, options = {}) {
    return this.request('/quiz/generate-flashcards', {
      method: 'POST',
      body: JSON.stringify({
        topic_id: topicId,
        num_cards: options.num_cards || 6,
        api_key: options.api_key
      })
    });
  }

  submitDynamicQuiz(payload) {
    return this.request('/quiz/submit-dynamic', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  }

  // Progress & Dashboard
  getDashboardStats() {
    return this.request('/dashboard/stats');
  }

  updateProgress(topicId, subtopicId, minutesSpent = 15, completionPercentage = 100) {
    return this.request('/progress', {
      method: 'POST',
      body: JSON.stringify({
        topic_id: topicId,
        subtopic_id: subtopicId,
        minutes_spent: minutesSpent,
        completion_percentage: completionPercentage
      })
    });
  }

  // Skill Gap Analysis
  getSkillGaps() {
    return this.request('/skill-gap');
  }

  // Recommendations
  getRecommendations() {
    return this.request('/recommendations');
  }

  // Chatbot
  sendMessage(message) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message })
    });
  }

  getChatHistory() {
    return this.request('/chat/history');
  }

  // Voice Assistant
  voiceToText(formDataOrData) {
    if (formDataOrData instanceof FormData) {
      return this.request('/voice-to-text', {
        method: 'POST',
        body: formDataOrData
      });
    }
    return this.request('/voice-to-text', {
      method: 'POST',
      body: JSON.stringify(formDataOrData)
    });
  }

  textToSpeech(text) {
    return this.request('/text-to-speech', {
      method: 'POST',
      body: JSON.stringify({ text })
    });
  }
}

export const api = new ApiService();
export default api;
