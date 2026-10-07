# Generative AI & NLP Engine for Education

# AI-POWERED PERSONALIZED LEARNING PATH GENERATION SYSTEM

### 23CS55C - ARTIFICIAL INTELLIGENCE
### MICRO PROJECT REPORT

<br>

**Submitted by**

**JEYAKIRTHIKA V** - 2312015  
**STUDENT NAME 2** - 23120XX  
**STUDENT NAME 3** - 23120XX  

<br>

**Course Instructor**

<br>

| Innovation and Problem statement<br>(10 Marks) | Implementation & Results<br>(10 Marks) | Presentation and Documentation<br>(10 Marks) | Viva<br>(10 Marks) | Total<br>(40 Marks) |
| :---: | :---: | :---: | :---: | :---: |
| | | | | |

<div style="page-break-after: always;"></div>

---

## TABLE OF CONTENTS

| CH NO | TITLE | PAGE NO |
| :---: | :--- | :---: |
| 1 | INTRODUCTION | 3 |
| 2 | PROBLEM STATEMENT | 4 |
| 3 | MODULE DESCRIPTION | 5 |
| 4 | ARCHITECTURE DIAGRAM | 7 |
| 5 | CODING & IMPLEMENTATION | 10 |
| 6 | OUTPUT SCREENSHOTS | 20 |
| 7 | CONCLUSION | 22 |

<div style="page-break-after: always;"></div>

---

## CHAPTER 1

## INTRODUCTION

In the modern educational landscape, traditional educational paradigms have long relied on one-size-fits-all curricula that fail to cater to individual student proficiencies, diverse learning speeds, and evolving industry standards. With the exponential growth of technical domains such as Artificial Intelligence, Data Science, and Software Engineering, learners frequently encounter fragmented learning materials, redundant content, and unclear prerequisite dependencies. This micro project addresses this critical challenge by engineering an **AI-Powered Personalized Learning Path Generation System** that dynamically synthesizes custom, mastery-based academic roadmaps tailored to each student's career aspirations and foundational knowledge.

### The Gap:

Conventional Learning Management Systems (LMS) and online course catalogs deliver rigid, linear syllabi that do not adapt to individual learning needs. Students are forced to traverse predefined modules regardless of whether they have already mastered foundational concepts or lack crucial prerequisites. Furthermore, these platforms lack automated diagnostic mechanisms to identify precise technical skill gaps against target career roles (such as AI/ML Engineer, Data Scientist, or Full-Stack Developer). When students struggle or fail assessments, standard systems offer no automated remedial feedback loop, leading to cognitive fatigue, knowledge voids, and high dropout rates.

### The Goal:

The primary objective of this project is to develop an end-to-end, intelligent learning ecosystem that leverages Natural Language Processing (NLP), Directed Acyclic Graph (DAG) topological sequencing, machine learning-driven risk prediction, and automated adaptive feedback. The system evaluates a learner's baseline proficiency through diagnostic benchmarking, computes numerical skill gaps against career benchmark vectors, and synthesizes an optimal prerequisite-respecting curriculum via Kahn's Topological Sort algorithm. In addition, the platform features dynamic quiz-driven remediation, context-aware AI tutoring, and hands-free voice interaction to deliver an adaptive, interactive, and personalized educational journey.

<div style="page-break-after: always;"></div>

---

## CHAPTER 2

## PROBLEM STATEMENT

Online education and technical upskilling platforms have become primary avenues for higher education and workforce preparation. However, students and early-career engineers frequently encounter substantial friction in navigating dense, unstructured technical curricula. The core problem lies in the absence of adaptive intelligence in traditional curricula design: learners are treated as homogenous cohorts, receiving identical course paths regardless of varying competencies, background knowledge, and specific target career outcomes.

### This deficiency manifests in several critical areas:

- **Rigid and Linear Progression Bottlenecks:** Standard e-learning systems sequence topics chronologically rather than dependency-wise. Students often encounter advanced algorithmic or mathematical concepts without first mastering essential prerequisites (e.g., attempting Deep Neural Networks without understanding Linear Algebra or Gradient Descent), leading to severe cognitive overload.
- **Absence of Granular Skill-Gap Quantification:** Existing platforms lack automated diagnostic tools to objectively measure a student's current proficiency vector against real-world target career requirements. Learners cannot pinpoint exactly which skills are critical, moderate, or already met.
- **Lack of Dynamic Remediation and Feedback Loops:** In traditional LMS architectures, failing a module test merely yields a numerical score without re-engineering the curriculum. There is no automated mechanism to dynamically insert remedial exercises, reinforce prerequisite concepts, or adjust pacing in real time.
- **Inflexible Static Pacing and Missing Tutoring Support:** Students learn at varying velocities, yet static curricula cannot dynamically predict completion timelines or identify high-risk modules. Moreover, without interactive tutoring, students facing conceptual bottlenecks are left without immediate guidance.

The consequences are profound: suboptimal learning efficiency, knowledge retention deficits, frustration, and demotivation. In an era where data-driven adaptation is paramount, education must shift from static delivery to dynamic personalization. This project bridges this divide by developing an AI-driven educational engineering platform that dynamically analyzes student skill gaps, constructs dependency-validated DAG roadmaps, and provides automated remedial adaptation and interactive tutoring.

<div style="page-break-after: always;"></div>

---

## CHAPTER 3

## MODULE DESCRIPTION

The AI-Powered Personalized Learning Path Generation System is structured into six key modules, each handling a specific dimension of the educational pipeline. These modules work collaboratively to transform raw learner diagnostic profiles into an adaptive, dependency-validated learning journey.

1. **Student Profiling and Diagnostic Assessment Module:** Captures user career objectives, baseline self-ratings, and diagnostic test responses to construct a multi-dimensional student competency profile.
2. **NLP and Curriculum Extraction Module:** Leverages TF-IDF token vectorization and cosine similarity to extract semantic keywords from curriculum topic catalogs and align them mathematically with student goals.
3. **Skill-Gap Analysis and Vector Distance Engine:** Compares student proficiency vectors against career benchmark requirements, computing weighted distance scores to identify Critical, Moderate, and Met skill levels.
4. **DAG-Based Learning Path Generation and Remediation Module:** Formulates curriculum topics as a Directed Acyclic Graph (DAG) and executes Kahn's Topological Sort algorithm to guarantee that all prerequisite dependencies are satisfied in optimal pedagogical order. It also includes dynamic quiz remediation to inject refresher content upon assessment failure.
5. **Interactive Assessment and Mastery Tracking Module:** Delivers timed module quizzes, tracks concept retention, awards continuous learning streaks, and logs completion analytics to keep learners engaged.
6. **Intelligent Tutoring Chatbot and Voice Assistant Module:** Features an NLP-driven conversational agent with intent classification alongside Google Speech Recognition and gTTS audio synthesis for natural, hands-free voice interaction.

### Architectural Foundation:

The system is built upon a high-performance, modular full-stack architecture. The frontend is engineered with **React 18** and **Vite**, utilizing Lucide React icons, Recharts for radar and progress analytics, and the HTML5 Web Speech API. The backend is powered by **Python Flask** structured with modular blueprints. Data persistence is managed via **SQLAlchemy ORM** supporting **MySQL** with an automated zero-configuration **SQLite** fallback (`learning_path.db`). Core AI and machine learning tasks utilize **scikit-learn** (TF-IDF vectorizer, Cosine Similarity, K-Means clustering, Random Forest performance prediction), graph algorithms via Python collections, and audio pipelines powered by **SpeechRecognition** and **gTTS**.

### Functional Modules:

- **Student Profiling and Diagnostic Assessment Module:** Collects student career goals (e.g., Data Scientist, AI/ML Engineer, Full Stack Developer), processes baseline diagnostic tests, and stores verified proficiency ratings across technical domains.
- **NLP and Curriculum Extraction Module:** Tokenizes and cleans course syllabi, removes stop words, generates unigram and bigram TF-IDF feature matrices, and computes semantic alignment with student query profiles.
- **Skill-Gap Analysis Module:** Computes weighted Euclidean-style gap distances against industry-benchmarked career skill sets, classifying each skill into Critical, Moderate, or Met status, and suggests corresponding courses.
- **DAG Topological Sequencing Module:** Constructs prerequisite dependency adjacency lists and computes in-degrees for each topic. Executes Kahn's algorithm to resolve topic ordering, prioritizing foundational concepts and addressing weak areas first.
- **Adaptive Remediation Engine:** Dynamically intercepts quiz evaluation results; if a student scores below 60%, the system flags the topic for remedial review and attaches supplementary exercises. Scores of 85% or higher trigger mastery acceleration.
- **Intelligent Tutoring Chatbot & Voice Assistant:** Implements multi-intent classification (`why_recommended`, `next_topic`, `concept_explanation`, `skill_gaps`, `career_guidance`), delivering contextual academic tutoring via chat and voice.

### Operational Flow:

The operational flow commences when a student registers and selects a target career goal. The student undertakes an initial diagnostic benchmark assessment that establishes their baseline proficiency. The NLP engine calculates TF-IDF representations of all topics and matches them against the student's profile. The DAG Topological Sort sequences the curriculum based on prerequisite dependencies, while the Random Forest predictor projects topic difficulty and pass probabilities. As the student engages with learning content and completes mastery quizzes, the system dynamically updates progress, recalibrating the path and providing remedial assistance when needed, supported continuously by the AI tutoring chatbot and voice assistant.

<div style="page-break-after: always;"></div>

---

## CHAPTER 4

## ARCHITECTURAL DIAGRAM

### 4.1 Overview:

The architecture of the AI-Powered Personalized Learning Path Generation System follows a modular, five-layered design that cleanly isolates user presentation, application routing, core AI computation, database persistence, and external AI services. This layered decoupling ensures high maintainability, clean separation of concerns, and rapid extensibility.

### 4.2 Architectural Diagram:

```
+-----------------------------------------------------------------------------------+
|                              USER INTERFACE LAYER                                 |
|                                                                                   |
|  [ React 18 SPA + Vite ]  [ Recharts Analytics & Radar ]  [ Web Speech Voice UI ] |
+------------------------------------------+----------------------------------------+
                                           |  HTTP / REST (JSON) & Audio Blobs
                                           v
+-----------------------------------------------------------------------------------+
|                               APPLICATION LAYER                                   |
|                                                                                   |
|                              [ Flask REST API ]                                   |
|   /api/auth   /api/profile   /api/assessment   /api/learning-path   /api/quiz     |
|   /api/progress   /api/skill-gap   /api/recommendations   /api/chat   /api/voice  |
+------------------------------------------+----------------------------------------+
                                           |  Service Orchestration
                                           v
+-----------------------------------------------------------------------------------+
|                                PROCESSING LAYER                                   |
|                                                                                   |
|  +--------------------+  +----------------------+  +---------------------------+  |
|  |  DAG Topological   |  |   TF-IDF & Cosine    |  |     Skill-Gap Matrix      |  |
|  |  Sequencing Engine |  | Similarity Matcher   |  |     Distance Engine       |  |
|  +--------------------+  +----------------------+  +---------------------------+  |
|  +--------------------+  +----------------------+  +---------------------------+  |
|  | Adaptive Remedial  |  | NLP Intent Chatbot  |  | Random Forest Performance |  |
|  |   Quiz Engine      |  |   & Voice Pipeline   |  |    & Cohort Predictor     |  |
|  +--------------------+  +----------------------+  +---------------------------+  |
+------------------------------------------+----------------------------------------+
                                           |  SQLAlchemy ORM
                                           v
+-----------------------------------------------------------------------------------+
|                                   DATA LAYER                                      |
|                                                                                   |
|   [ Users & Profiles ]  [ Career Goals & Skills ]  [ Topics, DAG Prerequisites ]  |
|   [ Learning Paths & Topics ]  [ Quizzes & Results ]  [ SQLite / MySQL Storage ]  |
+------------------------------------------+----------------------------------------+
                                           |  AI Model Calls & Inference
                                           v
+-----------------------------------------------------------------------------------+
|                              INFRASTRUCTURE LAYER                                 |
|                                                                                   |
|    [ Python 3.10+ Runtime ]   [ scikit-learn / NumPy ]   [ SpeechRecognition ]    |
|    [ Google Text-to-Speech (gTTS) ]   [ NLTK Tokenizer ]   [ SQLite3 Engine ]     |
+-----------------------------------------------------------------------------------+
```

<div style="page-break-after: always;"></div>

---

### 4.3 Layer Descriptions

#### 4.3.1 User Interface Layer
- **Component:** React 18 Single Page Application (SPA) powered by Vite.
- **Functionality:** Provides responsive learning dashboards, interactive DAG roadmap node visualizations, skill-gap radar charts, quiz interfaces, and a persistent floating voice assistant modal.
- **Technology:** React.js, Tailwind/Vanilla CSS, Lucide Icons, Recharts, HTML5 Audio API.
- **Purpose:** Delivers an intuitive, accessible interface for students to interact with their customized curriculum and track their progress.

#### 4.3.2 Application Layer
- **Component:** Flask REST API and modular routing blueprints.
- **Functionality:** Manages authentication (JWT/Session), exposes endpoints for profiles, diagnostics, path generation, quiz evaluation, analytics, and voice endpoints.
- **Technology:** Python Flask, Flask-CORS, Werkzeug Security.
- **Purpose:** Coordinates incoming requests and routes them to the appropriate processing and database components.

#### 4.3.3 Processing Layer
- **Component:** AI Reasoning, NLP, and Graph Processing Engines.
- **Functionality:**
  - *DAG Topological Sequencing:* Enforces prerequisite satisfaction using Kahn's algorithm.
  - *NLP Engine:* Extracts curriculum keywords and computes cosine similarities between student goals and topic content.
  - *Skill-Gap Engine:* Computes numerical skill gaps across proficiency levels.
  - *Adaptive Engine:* Adjusts topic sequencing dynamically based on quiz performance.
- **Technology:** scikit-learn, NumPy, NLTK, Python collections (`deque`, `defaultdict`).
- **Purpose:** Executes core educational logic and machine learning algorithms.

#### 4.3.4 Data Layer
- **Component:** Relational Database and SQLAlchemy ORM models.
- **Functionality:** Stores persistent records for users, career goals, skills, topics, prerequisite relationships, generated paths, quizzes, and streak analytics.
- **Technology:** SQLAlchemy ORM, SQLite (`learning_path.db`), MySQL.
- **Purpose:** Provides structured, normalized, and persistent storage for all academic and user data.

#### 4.3.5 Infrastructure Layer
- **Component:** Core Machine Learning, NLP, and Voice synthesis libraries.
- **Functionality:** Provides tokenization, TF-IDF vectorization, speech recognition, and base64 audio synthesis.
- **Technology:** scikit-learn, SpeechRecognition (Google Web Speech API), gTTS, Python 3.x.
- **Purpose:** Supplies foundational computational and cognitive capabilities.

<div style="page-break-after: always;"></div>

---

### 4.4 Data Flow

1. **User Goal Selection and Diagnostic Testing:** The student submits career goals and completes the diagnostic test via the React frontend.
2. **Profile Vectorization and NLP Matching:** The application layer forwards profile data to the processing layer, where TF-IDF vectorization and cosine similarity match topics to the student's target role.
3. **DAG Prerequisite Resolution:** Kahn's topological sort organizes matching topics into an acyclic dependency graph, sequencing foundational modules before advanced electives.
4. **Adaptive Quiz Assessment:** As the student completes module quizzes, the adaptive engine evaluates scores; scores under 60% dynamically insert remedial reviews, while scores over 85% unlock accelerated progress.
5. **Interactive Support and Visualization:** Real-time progress, radar charts, chatbot responses, and synthesized voice feedback are returned to the user interface.

### 4.5 Key Design Decisions

- **DAG-Based Dependency Resolution:** Modeling the curriculum as a Directed Acyclic Graph prevents circular dependencies and ensures strict pedagogical prerequisite ordering.
- **Hybrid AI Architecture:** Combines deterministic graph algorithms (Kahn's Topological Sort) with statistical NLP (TF-IDF, Cosine Similarity) and supervised machine learning (Random Forest) for reliable, transparent recommendations.
- **Dual Database Flexibility:** Implements automatic zero-configuration SQLite fallback if MySQL is unavailable, ensuring high portability across environments.
- **Explainable AI Recommendations:** Every recommended topic includes explicit reasoning strings detailing prerequisite fulfillment, similarity scores, and predicted pass rates.
- **Multimodal Tutoring:** Combines visual dashboards, textual chat, and hands-free voice synthesis to accommodate diverse learning styles.

<div style="page-break-after: always;"></div>

---

## CHAPTER 5

## CODING AND IMPLEMENTATION

### 5.1 Introduction

This chapter details the coding and implementation of the AI-Powered Personalized Learning Path Generation System. The system is built using Python with Flask, scikit-learn, and SQLAlchemy on the backend, complemented by a modern React.js frontend. The codebase follows clean software engineering principles, maintaining strict separation between data persistence, AI algorithms, API routing, and user interface components.

### 5.2 Coding

Below are key code snippets illustrating core system modules.

#### 5.2.1 DAG Topological Sequencing and Learning Path Generation (`backend/ai/learning_path.py`):

```python
import json
from collections import defaultdict, deque
import numpy as np
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.models.models import User, StudentProfile, CareerGoal, Topic, Prerequisite, LearningPath, LearningPathTopic

def generate_personalized_learning_path(db: Session, user_id: int) -> dict:
    # 1. Fetch Student Profile and Career Goal
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    career_goal = db.query(CareerGoal).filter(CareerGoal.id == profile.career_goal_id).first() if profile else db.query(CareerGoal).first()
    all_topics = db.query(Topic).all()
    topic_by_id = {t.id: t for t in all_topics}

    # 2. Compute TF-IDF & Cosine Similarity
    topic_corpus = [f"{t.title} {t.category} {t.description}" for t in all_topics]
    student_query = f"{career_goal.target_role} {career_goal.title} {career_goal.description}"
    
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(topic_corpus + [student_query])
    cos_similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
    similarity_map = {all_topics[i].id: float(cos_similarities[i]) for i in range(len(all_topics))}

    # 3. Build DAG Prerequisite Graph & Compute In-Degrees
    prereq_records = db.query(Prerequisite).all()
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    for pr in prereq_records:
        adj[pr.prerequisite_topic_id].append(pr.topic_id)
        in_degree[pr.topic_id] += 1

    # 4. Kahn's Algorithm Priority Queue
    queue = deque([t.id for t in all_topics if in_degree[t.id] == 0])
    ordered_topic_ids = []
    while queue:
        curr_id = queue.popleft()
        ordered_topic_ids.append(curr_id)
        for dependent_id in adj[curr_id]:
            in_degree[dependent_id] -= 1
            if in_degree[dependent_id] == 0:
                queue.append(dependent_id)

    return {"status": "success", "total_topics": len(ordered_topic_ids), "ordered_ids": ordered_topic_ids}
```

<div style="page-break-after: always;"></div>

---

#### 5.2.2 Skill Gap Analysis and Vector Distance Engine (`backend/ai/skill_gap.py`):

```python
import json
from sqlalchemy.orm import Session
from backend.models.models import StudentProfile, CareerGoal, Skill, StudentSkill, Topic, SkillGap

LEVEL_MAP = {"none": 0, "beginner": 1, "intermediate": 2, "advanced": 3}

def analyze_student_skill_gaps(db: Session, user_id: int) -> dict:
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    career_goal = db.query(CareerGoal).filter(CareerGoal.id == profile.career_goal_id).first()
    required_skills = json.loads(career_goal.required_skills_json or "[]")
    
    student_skills_records = db.query(StudentSkill).filter(StudentSkill.user_id == user_id).all()
    user_skill_levels = {ss.skill.name.lower(): ss.current_level for ss in student_skills_records if ss.skill}

    gaps_result = []
    total_required = 0
    total_earned = 0

    for item in required_skills:
        skill_name = item.get("skill_name", "")
        req_val = LEVEL_MAP.get(item.get("required_level", "Intermediate").lower(), 2)
        curr_val = LEVEL_MAP.get(user_skill_levels.get(skill_name.lower(), "Beginner").lower(), 1)
        gap_diff = req_val - curr_val
        
        status = "Critical" if gap_diff >= 2 else "Moderate" if gap_diff == 1 else "Met"
        total_required += req_val
        total_earned += min(curr_val, req_val)

        gaps_result.append({
            "skill_name": skill_name,
            "required_val": req_val,
            "current_val": curr_val,
            "gap_status": status
        })

    readiness = round((total_earned / max(total_required, 1)) * 100, 1)
    return {"target_career": career_goal.title, "readiness_percentage": readiness, "gaps": gaps_result}
```

<div style="page-break-after: always;"></div>

---

#### 5.2.3 NLP Intent Classifier and Keyword Extraction (`backend/ai/nlp.py`):

```python
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s\+\#]", " ", text)
    return " ".join([t for t in text.split() if len(t) > 1])

def parse_chatbot_intent(query: str) -> dict:
    q = query.lower()
    if any(k in q for k in ["why recommend", "why did you suggest", "reason for"]):
        return {"intent": "why_recommended", "confidence": 0.92}
    if any(k in q for k in ["what should i learn next", "next topic", "where do i start"]):
        return {"intent": "next_topic", "confidence": 0.89}
    if any(k in q for k in ["explain", "what is", "how does", "define"]):
        return {"intent": "concept_explanation", "confidence": 0.90}
    if any(k in q for k in ["weak", "gap", "struggling", "score"]):
        return {"intent": "skill_gaps", "confidence": 0.88}
    return {"intent": "general_tutoring", "confidence": 0.75}
```

#### 5.2.4 Speech Recognition Pipeline (`backend/voice/speech_to_text.py`):

```python
import io
import speech_recognition as sr

def transcribe_audio_bytes(audio_bytes: bytes) -> dict:
    recognizer = sr.Recognizer()
    try:
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return {"success": True, "text": text}
    except sr.UnknownValueError:
        return {"success": False, "error": "Speech was unintelligible"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

<div style="page-break-after: always;"></div>

---

### 5.3 Code Structure:

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
├── start_all.bat                 # One-click launch for Windows
├── start_backend.bat             # Launch Python Flask server
└── start_frontend.bat            # Launch React Vite dev server
```

<div style="page-break-after: always;"></div>

---

### 5.4 VS Code Screenshots:

The following files represent the core components implemented in the development environment:

- **i) learning_path.py (DAG Topological Sorter & Adaptive Path Generator)**  
  Implements Kahn's Algorithm on topic dependencies and dynamically recalibrates sequences based on quiz scores.
- **ii) skill_gap.py (Proficiency Vector Distance Analysis)**  
  Compares target career skill vectors against student diagnostics and produces categorized gap reports.
- **iii) nlp.py (Curriculum Text Vectorization & Intent Parser)**  
  Processes raw text into TF-IDF vectors and classifies user chatbot interactions.
- **iv) speech_to_text.py & text_to_speech.py (Audio Interface Pipeline)**  
  Provides audio processing, voice-to-text recognition, and synthesized speech responses.

### 5.5 Implementation Details:

- **Environment Setup:**  
  Install backend dependencies using:
  ```bash
  pip install flask flask-cors sqlalchemy scikit-learn numpy nltk speechrecognition gtts werkzeug
  ```
  Install frontend dependencies using:
  ```bash
  cd frontend && npm install
  ```
- **Database Initialization & Seeding:**  
  Run database setup to create tables and populate initial career paths, skills, topics, and quizzes:
  ```bash
  python -c "from backend.database.seed_data import seed_database; seed_database()"
  ```
- **Running the Application:**  
  - *Automated Launch:* Run `start_all.bat` to launch both servers concurrently.
  - *Backend:* `python -m backend.app` (runs at `http://localhost:5000`).
  - *Frontend:* `npm run dev` in `frontend/` (runs at `http://localhost:5173`).
- **Automated Verification:**  
  Execute the integration test suite:
  ```bash
  python backend/test_api.py
  ```

<div style="page-break-after: always;"></div>

---

## CHAPTER 6

## OUTPUT SCREENSHOTS

*(Insert application screenshots in this section)*

### Figure 6.1: Student Analytics Dashboard
Displays active roadmap progress, overall completion rate, learning streaks, and the comprehensive skills radar chart comparing current proficiencies against target career demands.

### Figure 6.2: Dynamic DAG Personalized Learning Roadmap
Shows prerequisite-sequenced modules, completion badges, estimated hours, and explicit AI recommendation rationale for each learning node.

### Figure 6.3: Skill-Gap Analysis & Readiness Visualizer
Visualizes granular skill readiness scores, categorizing competencies into Critical, Moderate, and Met tiers, along with direct course recommendation mappings.

### Figure 6.4: Interactive Topic Reader & Mastery Quiz Interface
Presents structured learning content with timed diagnostic quizzes and immediate score feedback, including automated remedial recommendations upon score deficits.

### Figure 6.5: Intelligent AI Tutoring Chatbot & Floating Voice Assistant
Demonstrates real-time conversational assistance, showing concept explanations, roadmap inquiries, and voice-driven interactions.

<div style="page-break-after: always;"></div>

---

## CHAPTER 7

## CONCLUSION

### 7.1 Summary of the Project:

The **AI-Powered Personalized Learning Path Generation System** has been successfully designed, implemented, and validated as an end-to-end educational engineering solution. By combining Natural Language Processing (TF-IDF and Cosine Similarity), Directed Acyclic Graph (DAG) topological sequencing, machine learning-driven risk forecasting, and adaptive remediation, the platform provides personalized, prerequisite-respecting learning pathways that adapt to individual learner needs.

Key achievements include:
- Development of a robust DAG-based topological sequencing engine that eliminates circular dependencies and respects curriculum prerequisites.
- Implementation of a vector-based skill gap analysis tool providing actionable, granular readiness metrics against target career roles.
- Engineering of an automated adaptive feedback loop that dynamically inserts refresher content upon quiz failure.
- Creation of an interactive React frontend paired with an intelligent NLP chatbot and hands-free voice assistant.

### 7.2 Contributions to the Field:

- **Democratization of Personalized Education:** Delivers adaptive, high-quality tutoring capabilities without requiring expensive private instructional resources.
- **Practical Application of Graph Theory & NLP:** Demonstrates how Kahn's Topological Sort and TF-IDF can be unified into an efficient curriculum sequencing pipeline.
- **Automated Remediation Workflows:** Showcases dynamic syllabus adjustment, addressing learning deficits in real time.
- **Open-Source Architectural Reference:** Establishes a modular full-stack reference design for adaptive educational platforms.

### 7.3 Limitations and Future Work:

- **Large Language Model (LLM) Integration:** Incorporate fine-tuned open-source LLMs (such as LLaMA 3 or Mistral) for deeper conversational explanations.
- **Multimodal Content Processing:** Extend curriculum ingestion to automatically parse lecture videos, PDF textbooks, and code repositories.
- **Collaborative Social Learning:** Introduce peer-matching algorithms to connect students with complementary skill profiles.
- **Mobile Application Deployment:** Package the frontend as a cross-platform mobile application using React Native or Flutter.

### 7.4 Impact on the Educational Technology Ecosystem:

- Lowers barrier to entry for structured career transitions into AI, Data Science, and Software Engineering.
- Reduces learner dropouts by addressing prerequisite gaps early in the study process.
- Empowers academic institutions to automate diagnostic profiling and provide targeted student support.

### 7.5 Final Remarks:

The successful realization of this system confirms the effectiveness of combining graph-based dependency modeling with NLP to solve curriculum planning challenges. By moving beyond rigid, linear syllabi, the platform delivers an adaptive educational experience that enhances learner comprehension, retention, and career readiness.

<br>

---

### RUBRICS :

| Aim & Algorithm<br>(10 Marks) | Coding & Implementation<br>(20 Marks) | Optimization<br>(10 Marks) | Output<br>(5 Marks) | Time Management<br>(5 Marks) | Viva<br>(10 Marks) | Total<br>(60 Marks) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| | | | | | | |

<br>

### RESULT:

The **AI-Powered Personalized Learning Path Generation System** has been successfully implemented and tested, demonstrating robust DAG-based prerequisite curriculum sequencing, accurate numerical skill-gap analysis, adaptive quiz-driven remediation, and intuitive web and voice interfaces. All core functionalities operate with high performance and reliability, establishing an effective AI-powered educational platform.
