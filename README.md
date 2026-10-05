# AI-Powered Personalized Learning Path Generation System

An intelligent, full-stack educational engineering platform that dynamically computes student skill profiles, performs NLP extraction & skill-gap analysis, generates DAG topological sequenced learning roadmaps, tracks mastery via real-time interactive quizzes, and provides an integrated intelligent Python Chatbot and Voice Assistant.

---

## Architecture & Technology Stack

- **Frontend**:
  - React.js (v18+) with Vite
  - Lucide React Icons
  - Recharts for Radar, Bar, & Progress visualizations
  - Web Speech API + SpeechRecognition fallback
- **Backend**:
  - Python (Flask REST APIs)
  - Modular Blueprints: `auth`, `profile`, `assessment`, `learning_path`, `quiz`, `progress`, `skill_gap`, `recommendation`, `chatbot`, `voice`
- **Database**:
  - MySQL with SQLAlchemy ORM
  - Built-in automatic SQLite fallback (`learning_path.db`) for instant zero-config startup
  - Comprehensive relational schema: `database/schema.sql`
- **AI & NLP Engine**:
  - **DAG Topological Sort**: Sequences topics strictly respecting prerequisites
  - **TF-IDF & Cosine Similarity**: NLP matching of student interests and goals to curriculum topics
  - **Skill-Gap Matrix**: Numerical vector analysis comparing current proficiency against target role requirements
  - **Dynamic Adaptive Update**: Re-sequences learning paths on quiz failure to insert remediation topics
  - **K-Means / Classifier Modeling**: Clusters student learner archetypes and predicts completion milestones
- **Chatbot & Voice Assistant**:
  - Rule + NLP Intent Classification (`explain`, `next_topic`, `quiz`, `skill_gap`, `recommendation`)
  - Google Speech Recognition (`SpeechRecognition`) & Text-to-Speech synthesis (`gTTS`)

---

## Project Structure

```
d:/ainlp/
├── backend/
│   ├── ai/
│   │   ├── chatbot.py            # AI Chatbot with intent classification
│   │   ├── clustering.py         # K-Means learner clustering
│   │   ├── learning_path.py      # DAG Topological Sort & path generation
│   │   ├── nlp.py                # TF-IDF & Cosine similarity extraction
│   │   ├── predictor.py          # Random Forest score & timeline predictor
│   │   ├── recommendation.py     # Content-based & collaborative filtering
│   │   └── skill_gap.py          # Skill matrix distance & gap calculation
│   ├── database/
│   │   ├── db.py                 # SQLAlchemy connection with MySQL/SQLite fallback
│   │   ├── learning_path.db      # Local SQLite persistent store
│   │   └── seed_data.py          # Pre-populated careers, skills, topics & quizzes
│   ├── models/
│   │   └── models.py             # Declarative ORM models (Users, Paths, Quizzes)
│   ├── routes/
│   │   ├── auth_routes.py        # /api/register & /api/login
│   │   ├── profile_routes.py     # /api/profile (GET & PUT)
│   │   ├── assessment_routes.py  # Initial diagnostic skill evaluation
│   │   ├── learning_path_routes.py # Personalized DAG roadmap & re-generation
│   │   ├── quiz_routes.py        # Module mastery quizzes & grading
│   │   ├── progress_routes.py    # Time, completions, streak tracking
│   │   ├── skill_gap_routes.py   # Numerical skill gap breakdown
│   │   ├── recommendation_routes.py # AI personalized recommendations
│   │   ├── chatbot_routes.py     # Context-aware educational chatbot
│   │   └── voice_routes.py       # Speech-to-Text & Text-to-Speech pipeline
│   ├── voice/
│   │   ├── speech_to_text.py     # Audio decoding & speech recognition
│   │   └── text_to_speech.py     # Base64 audio synthesis
│   ├── app.py                    # Flask application entry point
│   ├── requirements.txt          # Python dependencies
│   └── test_api.py               # Automated end-to-end REST test suite
├── database/
│   └── schema.sql                # Complete MySQL DDL schema
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FloatingVoiceModal.jsx # Live voice assistant popup
│   │   │   ├── Header.jsx        # Navigation header & user status
│   │   │   └── Sidebar.jsx       # Tab routing sidebar
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx # Analytics, streak, radar, active path
│   │   │   ├── LearningPathPage.jsx # Interactive DAG timeline & filters
│   │   │   ├── SkillAssessmentPage.jsx # Diagnostic benchmark test
│   │   │   ├── SkillGapPage.jsx  # Radar & bar charts of missing skills
│   │   │   ├── TopicsListPage.jsx # Catalog of all courses & topics
│   │   │   ├── TopicLearningPage.jsx # Markdown reader & practice
│   │   │   ├── QuizPage.jsx      # Timed quiz with immediate evaluation
│   │   │   ├── ProgressTrackingPage.jsx # Learning stats & milestones
│   │   │   ├── RecommendationsPage.jsx # AI-curated electives
│   │   │   ├── ChatbotPage.jsx   # Dedicated tutoring chat assistant
│   │   │   └── ProfilePage.jsx   # Career goal & skill level editor
│   │   ├── services/
│   │   │   └── api.js            # Axios/Fetch client with auth headers
│   │   ├── App.jsx               # Main container with tab-based routing
│   │   └── index.css             # Glassmorphic, modern design system
│   ├── package.json
│   └── vite.config.js
├── .env.example
├── start_all.bat                 # One-click launch for Windows
├── start_backend.bat             # Launch Python Flask server
└── start_frontend.bat            # Launch React Vite dev server
```

---

## Quick Start (Windows)

### 1. One-Click Launch (Recommended)
Simply double-click:
```cmd
start_all.bat
```
This automatically starts both the Python Backend (port 5000) and the React Frontend (port 5173).

---

### 2. Manual Startup Commands

#### Terminal 1: Backend
```powershell
cd d:\ainlp
python -m backend.app
```
*Backend runs on `http://localhost:5000`.*
*The database automatically detects MySQL at `localhost:3306`. If MySQL is unavailable, it seamlessly falls back to the embedded SQLite database.*

#### Terminal 2: Frontend
```powershell
cd d:\ainlp\frontend
npm run dev
```
*Frontend runs on `http://localhost:5173`.*

---

## Default Demo Credentials

You can log in immediately using the pre-seeded demo student account:
- **Email**: `alex.morgan@example.com`
- **Password**: `password123`

You can also register any new student account directly from the login page!

---

## Verifying the System

You can run the automated end-to-end backend verification test anytime:
```powershell
cd d:\ainlp
python backend/test_api.py
```
This tests:
1. Student Authentication (`POST /api/login`)
2. Profile & Goal Retrieval (`GET /api/profile`)
3. DAG Learning Path Generation (`GET /api/learning-path`)
4. Skill-Gap Distance Analysis (`GET /api/skill-gap`)
5. Content Recommendations (`GET /api/recommendations`)
6. Context-Aware AI Chatbot (`POST /api/chat`)
7. Voice Assistant Audio Pipeline (`POST /api/voice-to-text`)
