-- ====================================================================
-- AI-Powered Personalized Learning Path Generation System
-- Relational MySQL Database Schema
-- ====================================================================

CREATE DATABASE IF NOT EXISTS learning_path_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE learning_path_db;

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. CAREER GOALS
CREATE TABLE IF NOT EXISTS career_goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL UNIQUE,
    target_role VARCHAR(150) NOT NULL,
    description TEXT,
    required_skills_json TEXT, -- JSON array of {skill_name, required_level, weight}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 3. STUDENT PROFILES
CREATE TABLE IF NOT EXISTS student_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    education_level VARCHAR(100) DEFAULT 'Undergraduate', -- High School, Undergraduate, Graduate, Working Professional
    experience_level VARCHAR(50) DEFAULT 'Beginner',     -- Beginner, Intermediate, Advanced
    interests TEXT,                                      -- e.g. "AI, Deep Learning, Natural Language Processing, Automation"
    career_goal_id INT,
    target_job_role VARCHAR(150) DEFAULT 'Data Scientist',
    overall_skill_level VARCHAR(50) DEFAULT 'Beginner',
    bio TEXT,
    streak_days INT DEFAULT 1,
    total_learning_minutes INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (career_goal_id) REFERENCES career_goals(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 4. SKILLS
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL, -- Programming, Mathematics, AI/ML, Data, Cloud, etc.
    description TEXT
) ENGINE=InnoDB;

-- 5. STUDENT SKILLS
CREATE TABLE IF NOT EXISTS student_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
    current_level VARCHAR(50) DEFAULT 'Beginner', -- Beginner, Intermediate, Advanced
    confidence_score FLOAT DEFAULT 0.0,           -- 0.0 to 1.0
    verified_by_assessment BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_skill (user_id, skill_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 6. TOPICS
CREATE TABLE IF NOT EXISTS topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    difficulty VARCHAR(50) DEFAULT 'Beginner', -- Beginner, Intermediate, Advanced
    estimated_hours INT DEFAULT 5,
    description TEXT,
    key_concepts_json TEXT, -- JSON array of core concepts
    resources_json TEXT,    -- JSON list of articles, tutorials, video links
    practice_exercises_json TEXT, -- JSON list of exercise tasks
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 7. SUBTOPICS
CREATE TABLE IF NOT EXISTS subtopics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    order_index INT NOT NULL DEFAULT 1,
    summary TEXT,
    learning_content MEDIUMTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 8. PREREQUISITES
CREATE TABLE IF NOT EXISTS prerequisites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic_id INT NOT NULL,
    prerequisite_topic_id INT NOT NULL,
    UNIQUE KEY uq_topic_prereq (topic_id, prerequisite_topic_id),
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    FOREIGN KEY (prerequisite_topic_id) REFERENCES topics(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 9. LEARNING PATHS
CREATE TABLE IF NOT EXISTS learning_paths (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    career_goal_id INT,
    title VARCHAR(250) NOT NULL,
    total_topics INT DEFAULT 0,
    completed_topics INT DEFAULT 0,
    overall_progress FLOAT DEFAULT 0.0,
    status VARCHAR(50) DEFAULT 'active', -- active, adapted, completed
    generated_by_algorithm VARCHAR(100) DEFAULT 'TFIDF-Cosine-DAG-Clustering',
    ai_reasoning TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (career_goal_id) REFERENCES career_goals(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 10. LEARNING PATH TOPICS
CREATE TABLE IF NOT EXISTS learning_path_topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    learning_path_id INT NOT NULL,
    topic_id INT NOT NULL,
    sequence_order INT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, completed, skipped, remedial
    score FLOAT DEFAULT NULL,
    recommended_reason TEXT,
    is_adaptive_addition BOOLEAN DEFAULT FALSE,
    estimated_learning_time VARCHAR(50) DEFAULT '6 hours',
    completed_at DATETIME DEFAULT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (learning_path_id) REFERENCES learning_paths(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 11. LEARNING PROGRESS
CREATE TABLE IF NOT EXISTS learning_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    topic_id INT NOT NULL,
    subtopic_id INT DEFAULT NULL,
    time_spent_minutes INT DEFAULT 0,
    completion_percentage FLOAT DEFAULT 0.0,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    FOREIGN KEY (subtopic_id) REFERENCES subtopics(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 12. ASSESSMENTS
CREATE TABLE IF NOT EXISTS assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    total_questions INT DEFAULT 10,
    time_limit_minutes INT DEFAULT 15,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 13. ASSESSMENT QUESTIONS
CREATE TABLE IF NOT EXISTS assessment_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT NOT NULL,
    topic_id INT,
    question_text TEXT NOT NULL,
    options_json TEXT NOT NULL, -- JSON array of 4 choices
    correct_answer VARCHAR(255) NOT NULL,
    difficulty VARCHAR(50) DEFAULT 'Intermediate',
    explanation TEXT,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 14. ASSESSMENT RESULTS
CREATE TABLE IF NOT EXISTS assessment_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    assessment_id INT NOT NULL,
    total_score INT NOT NULL,
    max_score INT NOT NULL,
    percentage FLOAT NOT NULL,
    skill_level_assigned VARCHAR(50) NOT NULL, -- Beginner, Intermediate, Advanced
    strong_topics_json TEXT,
    weak_topics_json TEXT,
    topic_breakdown_json TEXT,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 15. QUIZZES
CREATE TABLE IF NOT EXISTS quizzes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    difficulty VARCHAR(50) DEFAULT 'Intermediate',
    time_limit_minutes INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 16. QUIZ QUESTIONS
CREATE TABLE IF NOT EXISTS quiz_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id INT NOT NULL,
    question_text TEXT NOT NULL,
    options_json TEXT NOT NULL,
    correct_answer VARCHAR(255) NOT NULL,
    explanation TEXT,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 17. QUIZ RESULTS
CREATE TABLE IF NOT EXISTS quiz_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    quiz_id INT NOT NULL,
    score INT NOT NULL,
    total_questions INT NOT NULL,
    percentage FLOAT NOT NULL,
    passed BOOLEAN DEFAULT FALSE,
    adaptive_action_taken VARCHAR(255) DEFAULT 'None',
    answers_breakdown_json TEXT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 18. SKILL GAPS
CREATE TABLE IF NOT EXISTS skill_gaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
    target_career_id INT,
    required_level VARCHAR(50) NOT NULL,
    current_level VARCHAR(50) NOT NULL,
    gap_status VARCHAR(50) NOT NULL, -- Critical, Moderate, Met, Advanced
    gap_score FLOAT NOT NULL,        -- Higher score = larger gap
    recommended_topic_id INT,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    FOREIGN KEY (target_career_id) REFERENCES career_goals(id) ON DELETE SET NULL,
    FOREIGN KEY (recommended_topic_id) REFERENCES topics(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 19. RECOMMENDATIONS
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_type VARCHAR(50) NOT NULL, -- topic, course, project, exercise, quiz
    item_title VARCHAR(255) NOT NULL,
    item_id INT DEFAULT NULL,
    score FLOAT DEFAULT 0.0,
    reasoning TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 20. CHAT HISTORY
CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role VARCHAR(50) NOT NULL, -- student, assistant
    message TEXT NOT NULL,
    context_topic_id INT DEFAULT NULL,
    intent_detected VARCHAR(100) DEFAULT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 21. VOICE INTERACTIONS
CREATE TABLE IF NOT EXISTS voice_interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    transcribed_text TEXT NOT NULL,
    confidence FLOAT DEFAULT 0.95,
    ai_response_text TEXT NOT NULL,
    audio_duration_seconds FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;
