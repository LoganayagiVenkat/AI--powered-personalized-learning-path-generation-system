from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from backend.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    skills = relationship("StudentSkill", back_populates="user", cascade="all, delete-orphan")
    learning_paths = relationship("LearningPath", back_populates="user", cascade="all, delete-orphan")
    learning_progress = relationship("LearningProgress", back_populates="user", cascade="all, delete-orphan")
    assessment_results = relationship("AssessmentResult", back_populates="user", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="user", cascade="all, delete-orphan")
    skill_gaps = relationship("SkillGap", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    voice_interactions = relationship("VoiceInteraction", back_populates="user", cascade="all, delete-orphan")

class CareerGoal(Base):
    __tablename__ = "career_goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), unique=True, nullable=False)
    target_role = Column(String(150), nullable=False)
    description = Column(Text)
    required_skills_json = Column(Text)  # List of {skill_name, required_level, weight}
    created_at = Column(DateTime, default=datetime.utcnow)

    profiles = relationship("StudentProfile", back_populates="career_goal")
    learning_paths = relationship("LearningPath", back_populates="career_goal")

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    education_level = Column(String(100), default="Undergraduate")
    experience_level = Column(String(50), default="Beginner")
    interests = Column(Text, default="Machine Learning, Data Science, Python")
    career_goal_id = Column(Integer, ForeignKey("career_goals.id", ondelete="SET NULL"), nullable=True)
    target_job_role = Column(String(150), default="Data Scientist")
    overall_skill_level = Column(String(50), default="Beginner")
    bio = Column(Text, default="")
    streak_days = Column(Integer, default=1)
    total_learning_minutes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")
    career_goal = relationship("CareerGoal", back_populates="profiles")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text)

    student_skills = relationship("StudentSkill", back_populates="skill")

class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    current_level = Column(String(50), default="Beginner")  # Beginner, Intermediate, Advanced
    confidence_score = Column(Float, default=0.3)
    verified_by_assessment = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "skill_id", name="uq_user_skill"),)

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="student_skills")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    difficulty = Column(String(50), default="Beginner")
    estimated_hours = Column(Integer, default=5)
    description = Column(Text)
    key_concepts_json = Column(Text)  # JSON list
    resources_json = Column(Text)     # JSON list of articles/videos/docs
    practice_exercises_json = Column(Text) # JSON list
    created_at = Column(DateTime, default=datetime.utcnow)

    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="topic", cascade="all, delete-orphan")
    learning_path_topics = relationship("LearningPathTopic", back_populates="topic")

class Subtopic(Base):
    __tablename__ = "subtopics"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    order_index = Column(Integer, default=1)
    summary = Column(Text)
    learning_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    topic = relationship("Topic", back_populates="subtopics")

class Prerequisite(Base):
    __tablename__ = "prerequisites"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    prerequisite_topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("topic_id", "prerequisite_topic_id", name="uq_topic_prereq"),)

class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_goal_id = Column(Integer, ForeignKey("career_goals.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(250), nullable=False)
    total_topics = Column(Integer, default=0)
    completed_topics = Column(Integer, default=0)
    overall_progress = Column(Float, default=0.0)
    status = Column(String(50), default="active")  # active, completed, adapted
    generated_by_algorithm = Column(String(100), default="TFIDF-Cosine-DAG-Clustering")
    ai_reasoning = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="learning_paths")
    career_goal = relationship("CareerGoal", back_populates="learning_paths")
    path_topics = relationship("LearningPathTopic", back_populates="learning_path", cascade="all, delete-orphan", order_by="LearningPathTopic.sequence_order")

class LearningPathTopic(Base):
    __tablename__ = "learning_path_topics"

    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    sequence_order = Column(Integer, nullable=False)
    status = Column(String(50), default="pending")  # pending, in_progress, completed, skipped, remedial
    score = Column(Float, nullable=True)
    recommended_reason = Column(Text)
    is_adaptive_addition = Column(Boolean, default=False)
    estimated_learning_time = Column(String(50), default="6 hours")
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    learning_path = relationship("LearningPath", back_populates="path_topics")
    topic = relationship("Topic", back_populates="learning_path_topics")

class LearningProgress(Base):
    __tablename__ = "learning_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id", ondelete="SET NULL"), nullable=True)
    time_spent_minutes = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)
    last_accessed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="learning_progress")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text)
    total_questions = Column(Integer, default=10)
    time_limit_minutes = Column(Integer, default=15)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    question_text = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False)  # JSON list
    correct_answer = Column(String(255), nullable=False)
    difficulty = Column(String(50), default="Intermediate")
    explanation = Column(Text)

    assessment = relationship("Assessment", back_populates="questions")

class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    total_score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    skill_level_assigned = Column(String(50), nullable=False)  # Beginner, Intermediate, Advanced
    strong_topics_json = Column(Text)
    weak_topics_json = Column(Text)
    topic_breakdown_json = Column(Text)
    taken_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessment_results")

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    difficulty = Column(String(50), default="Intermediate")
    time_limit_minutes = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)

    topic = relationship("Topic", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text)

    quiz = relationship("Quiz", back_populates="questions")

class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    passed = Column(Boolean, default=False)
    adaptive_action_taken = Column(String(255), default="None")
    answers_breakdown_json = Column(Text)
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz_results")

class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    target_career_id = Column(Integer, ForeignKey("career_goals.id", ondelete="SET NULL"), nullable=True)
    required_level = Column(String(50), nullable=False)
    current_level = Column(String(50), nullable=False)
    gap_status = Column(String(50), nullable=False)  # Critical, Moderate, Met, Advanced
    gap_score = Column(Float, nullable=False)
    recommended_topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="skill_gaps")
    skill = relationship("Skill")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_type = Column(String(50), nullable=False)  # topic, course, project, exercise, quiz
    item_title = Column(String(255), nullable=False)
    item_id = Column(Integer, nullable=True)
    score = Column(Float, default=0.0)
    reasoning = Column(Text, nullable=False)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="recommendations")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False)  # student, assistant
    message = Column(Text, nullable=False)
    context_topic_id = Column(Integer, nullable=True)
    intent_detected = Column(String(100), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_history")

class VoiceInteraction(Base):
    __tablename__ = "voice_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    transcribed_text = Column(Text, nullable=False)
    confidence = Column(Float, default=0.95)
    ai_response_text = Column(Text, nullable=False)
    audio_duration_seconds = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="voice_interactions")
