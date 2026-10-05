import json
import logging
import uuid
import time
from flask import Blueprint, request, jsonify
from backend.database.db import get_db
from backend.models.models import (
    Quiz, QuizQuestion, QuizResult, Topic, StudentSkill, Skill
)
from backend.routes.profile_routes import get_current_user_id
from backend.ai.learning_path import adapt_learning_path_on_quiz
from backend.ai.quiz_generator import generate_dynamic_quiz_questions, generate_flashcards

logger = logging.getLogger("learning_path.quiz")
quiz_bp = Blueprint("quiz", __name__)

# Temporary in-memory cache for dynamic quiz sessions
ACTIVE_DYNAMIC_QUIZZES = {}

@quiz_bp.route("/api/quiz/<int:topic_id>", methods=["GET"])
def get_topic_quiz(topic_id: int):
    db = next(get_db())
    try:
        quiz = db.query(Quiz).filter(Quiz.topic_id == topic_id).first()
        if not quiz:
            # Create a quiz on the fly if needed
            topic = db.query(Topic).filter(Topic.id == topic_id).first()
            if not topic:
                return jsonify({"error": "Topic not found"}), 404
            quiz = Quiz(
                topic_id=topic.id,
                title=f"{topic.title} Mastery Evaluation",
                difficulty=topic.difficulty,
                time_limit_minutes=10
            )
            db.add(quiz)
            db.flush()

            # Add default questions
            db.add_all([
                QuizQuestion(
                    quiz_id=quiz.id,
                    question_text=f"Which core concept represents the primary principle of {topic.title}?",
                    options_json=json.dumps([
                        f"Algorithmic paradigms and best practices in {topic.category}",
                        "Static manual calculations without reproducibility",
                        "Ignoring edge cases and error bounds",
                        "Random guesswork without data"
                    ]),
                    correct_answer=f"Algorithmic paradigms and best practices in {topic.category}",
                    explanation=f"Foundational mastery of {topic.category} principles is essential."
                ),
                QuizQuestion(
                    quiz_id=quiz.id,
                    question_text=f"In production scenarios, how does {topic.title} prevent errors?",
                    options_json=json.dumps([
                        "Rigorous validation, metrics tracking, and error handling",
                        "Silencing all exceptions and warnings",
                        "Assuming all inputs are always clean and complete",
                        "Skipping test suites"
                    ]),
                    correct_answer="Rigorous validation, metrics tracking, and error handling",
                    explanation="Robust engineering requires systematic validation."
                )
            ])
            db.commit()

        questions = []
        for q in quiz.questions:
            questions.append({
                "id": q.id,
                "question_text": q.question_text,
                "options": json.loads(q.options_json),
                "explanation": q.explanation
            })

        topic = quiz.topic
        return jsonify({
            "quiz_id": quiz.id,
            "topic_id": topic.id if topic else topic_id,
            "topic_title": topic.title if topic else "Topic",
            "title": quiz.title,
            "difficulty": quiz.difficulty,
            "time_limit_minutes": quiz.time_limit_minutes,
            "total_questions": len(questions),
            "questions": questions
        }), 200
    finally:
        db.close()

@quiz_bp.route("/api/quiz", methods=["POST"])
def submit_quiz():
    user_id = get_current_user_id()
    data = request.get_json() or {}
    quiz_id = data.get("quiz_id")
    topic_id = data.get("topic_id")
    answers = data.get("answers", {})

    if not quiz_id:
        return jsonify({"error": "quiz_id is required"}), 400

    db = next(get_db())
    try:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404

        total_questions = len(quiz.questions)
        correct_count = 0
        answers_breakdown = []

        for q in quiz.questions:
            user_ans = answers.get(str(q.id))
            is_correct = (user_ans == q.correct_answer)
            if is_correct:
                correct_count += 1

            answers_breakdown.append({
                "question_id": q.id,
                "question_text": q.question_text,
                "selected_answer": user_ans,
                "correct_answer": q.correct_answer,
                "is_correct": is_correct,
                "explanation": q.explanation
            })

        percentage = round((correct_count / max(total_questions, 1)) * 100, 1)
        passed = (percentage >= 70.0)

        # Trigger Adaptive Learning Update on student's learning path
        t_id = topic_id or quiz.topic_id
        adaptive_outcome = adapt_learning_path_on_quiz(db, user_id, quiz_id, percentage, t_id)

        # Save Quiz Result
        result_record = QuizResult(
            user_id=user_id,
            quiz_id=quiz.id,
            score=correct_count,
            total_questions=total_questions,
            percentage=percentage,
            passed=passed,
            adaptive_action_taken=adaptive_outcome.get("action", "None"),
            answers_breakdown_json=json.dumps(answers_breakdown)
        )
        db.add(result_record)

        # Update student skill level
        topic = quiz.topic
        if topic:
            skill = db.query(Skill).filter(Skill.name.ilike(f"%{topic.title[:6]}%")).first()
            if skill:
                st_skill = db.query(StudentSkill).filter(
                    StudentSkill.user_id == user_id,
                    StudentSkill.skill_id == skill.id
                ).first()
                if st_skill:
                    if percentage >= 85.0:
                        st_skill.current_level = "Advanced"
                    elif percentage >= 60.0:
                        st_skill.current_level = "Intermediate"
                    st_skill.confidence_score = round(percentage / 100.0, 2)
                    st_skill.verified_by_assessment = True

        db.commit()

        return jsonify({
            "message": "Quiz submitted and evaluated successfully",
            "score": correct_count,
            "total_questions": total_questions,
            "percentage": percentage,
            "passed": passed,
            "adaptive_action": adaptive_outcome.get("action"),
            "new_overall_progress": adaptive_outcome.get("new_progress"),
            "answers_breakdown": answers_breakdown
        }), 201

    except Exception as e:
        db.rollback()
        logger.error(f"Error submitting quiz: {e}")
        return jsonify({"error": "Failed to submit quiz"}), 500
    finally:
        db.close()

@quiz_bp.route("/api/quiz/generate", methods=["POST"])
def generate_quiz_endpoint():
    data = request.get_json() or {}
    topic_id = data.get("topic_id", 1)
    num_questions = int(data.get("num_questions", 5))
    difficulty = data.get("difficulty", "Intermediate")
    focus_type = data.get("focus_type", "conceptual")
    api_key = data.get("api_key")

    db = next(get_db())
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return jsonify({"error": "Topic not found"}), 404

        topic_info = {
            "id": topic.id,
            "title": topic.title,
            "category": topic.category,
            "difficulty": difficulty or topic.difficulty,
            "description": topic.description,
            "concepts": json.loads(topic.key_concepts_json) if topic.key_concepts_json else [],
            "subtopics": [{"title": st.title, "summary": st.summary} for st in topic.subtopics]
        }

        generated_questions = generate_dynamic_quiz_questions(
            topic_data=topic_info,
            num_questions=num_questions,
            difficulty=difficulty,
            focus_type=focus_type,
            api_key=api_key
        )

        session_id = f"dyn_{uuid.uuid4().hex[:12]}"
        ACTIVE_DYNAMIC_QUIZZES[session_id] = {
            "topic_id": topic.id,
            "topic_title": topic.title,
            "created_at": time.time(),
            "questions": generated_questions
        }

        # Clean old sessions (> 2 hours)
        now = time.time()
        for k in list(ACTIVE_DYNAMIC_QUIZZES.keys()):
            if now - ACTIVE_DYNAMIC_QUIZZES[k]["created_at"] > 7200:
                ACTIVE_DYNAMIC_QUIZZES.pop(k, None)

        # Build client-safe payload (exclude correct_answer to prevent client-side inspection)
        client_questions = []
        for q in generated_questions:
            client_questions.append({
                "id": q["id"],
                "question_text": q["question_text"],
                "options": q["options"]
            })

        return jsonify({
            "session_id": session_id,
            "topic_id": topic.id,
            "topic_title": topic.title,
            "difficulty": difficulty,
            "focus_type": focus_type,
            "total_questions": len(client_questions),
            "questions": client_questions
        }), 200
    except Exception as e:
        logger.error(f"Error generating dynamic quiz: {e}")
        return jsonify({"error": f"Failed to generate dynamic quiz: {str(e)}"}), 500
    finally:
        db.close()

@quiz_bp.route("/api/quiz/generate-flashcards", methods=["POST"])
def generate_flashcards_endpoint():
    data = request.get_json() or {}
    topic_id = data.get("topic_id", 1)
    num_cards = int(data.get("num_cards", 6))
    api_key = data.get("api_key")

    db = next(get_db())
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return jsonify({"error": "Topic not found"}), 404

        topic_info = {
            "id": topic.id,
            "title": topic.title,
            "category": topic.category,
            "difficulty": topic.difficulty,
            "description": topic.description,
            "concepts": json.loads(topic.key_concepts_json) if topic.key_concepts_json else []
        }

        cards = generate_flashcards(topic_data=topic_info, num_cards=num_cards, api_key=api_key)
        return jsonify({
            "topic_id": topic.id,
            "topic_title": topic.title,
            "category": topic.category,
            "total_cards": len(cards),
            "flashcards": cards
        }), 200
    except Exception as e:
        logger.error(f"Error generating flashcards: {e}")
        return jsonify({"error": f"Failed to generate flashcards: {str(e)}"}), 500
    finally:
        db.close()

@quiz_bp.route("/api/quiz/submit-dynamic", methods=["POST"])
def submit_dynamic_quiz():
    user_id = get_current_user_id()
    data = request.get_json() or {}
    session_id = data.get("session_id")
    topic_id = data.get("topic_id")
    answers = data.get("answers", {})

    session_data = ACTIVE_DYNAMIC_QUIZZES.get(session_id)
    if not session_data:
        # Fallback if session expired or not found: if answers provided with raw questions
        questions = data.get("questions")
        if not questions:
            return jsonify({"error": "Dynamic quiz session expired or invalid. Please generate a new quiz."}), 400
    else:
        questions = session_data["questions"]
        topic_id = session_data.get("topic_id", topic_id)

    total_questions = len(questions)
    correct_count = 0
    answers_breakdown = []

    for q in questions:
        qid_str = str(q.get("id"))
        user_ans = answers.get(qid_str)
        corr_ans = q.get("correct_answer")
        is_correct = (user_ans == corr_ans)
        if is_correct:
            correct_count += 1

        answers_breakdown.append({
            "question_id": q.get("id"),
            "question_text": q.get("question_text"),
            "selected_answer": user_ans,
            "correct_answer": corr_ans,
            "is_correct": is_correct,
            "explanation": q.get("explanation", "Good review of key topic principles.")
        })

    percentage = round((correct_count / max(total_questions, 1)) * 100, 1)
    passed = (percentage >= 70.0)

    db = next(get_db())
    try:
        # Trigger Adaptive Learning Update
        adaptive_outcome = adapt_learning_path_on_quiz(db, user_id, 0, percentage, topic_id)

        # Update student skill level
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if topic:
            skill = db.query(Skill).filter(Skill.name.ilike(f"%{topic.title[:6]}%")).first()
            if skill:
                st_skill = db.query(StudentSkill).filter(
                    StudentSkill.user_id == user_id,
                    StudentSkill.skill_id == skill.id
                ).first()
                if st_skill:
                    if percentage >= 85.0:
                        st_skill.current_level = "Advanced"
                    elif percentage >= 60.0:
                        st_skill.current_level = "Intermediate"
                    st_skill.confidence_score = round(percentage / 100.0, 2)
                    st_skill.verified_by_assessment = True

        db.commit()

        return jsonify({
            "message": "AI Dynamic Quiz evaluated successfully",
            "score": correct_count,
            "total_questions": total_questions,
            "percentage": percentage,
            "passed": passed,
            "adaptive_action": adaptive_outcome.get("action"),
            "new_overall_progress": adaptive_outcome.get("new_progress"),
            "answers_breakdown": answers_breakdown
        }), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Error evaluating dynamic quiz: {e}")
        return jsonify({"error": "Failed to submit dynamic quiz"}), 500
    finally:
        db.close()
