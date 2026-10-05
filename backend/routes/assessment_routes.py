import json
import logging
from flask import Blueprint, request, jsonify
from backend.database.db import get_db
from backend.models.models import (
    User, Assessment, AssessmentQuestion, AssessmentResult,
    StudentProfile, StudentSkill, Skill, Topic
)
from backend.routes.profile_routes import get_current_user_id
from backend.ai.learning_path import generate_personalized_learning_path
from backend.ai.skill_gap import analyze_student_skill_gaps

logger = logging.getLogger("learning_path.assessment")
assessment_bp = Blueprint("assessment", __name__)

@assessment_bp.route("/api/assessment", methods=["GET"])
def get_assessment():
    db = next(get_db())
    try:
        assessment = db.query(Assessment).first()
        if not assessment:
            return jsonify({"error": "No assessment found"}), 404

        questions = []
        for q in assessment.questions:
            questions.append({
                "id": q.id,
                "topic_id": q.topic_id,
                "topic_title": q.topic.title if q.topic else "General",
                "question_text": q.question_text,
                "options": json.loads(q.options_json),
                "difficulty": q.difficulty
            })

        return jsonify({
            "id": assessment.id,
            "title": assessment.title,
            "category": assessment.category,
            "description": assessment.description,
            "time_limit_minutes": assessment.time_limit_minutes,
            "total_questions": len(questions),
            "questions": questions
        }), 200
    finally:
        db.close()

@assessment_bp.route("/api/assessment", methods=["POST"])
def submit_assessment():
    user_id = get_current_user_id()
    data = request.get_json() or {}
    answers = data.get("answers", {})  # Map of { question_id: selected_answer }

    db = next(get_db())
    try:
        assessment = db.query(Assessment).first()
        if not assessment:
            return jsonify({"error": "Assessment not found"}), 404

        total_questions = len(assessment.questions)
        correct_count = 0
        topic_scores = {}  # { topic_title: { "correct": 0, "total": 0 } }
        detailed_answers = []

        for q in assessment.questions:
            t_name = q.topic.title if q.topic else "General"
            if t_name not in topic_scores:
                topic_scores[t_name] = {"correct": 0, "total": 0}
            topic_scores[t_name]["total"] += 1

            user_ans = answers.get(str(q.id))
            is_correct = (user_ans == q.correct_answer)

            if is_correct:
                correct_count += 1
                topic_scores[t_name]["correct"] += 1

            detailed_answers.append({
                "question_id": q.id,
                "question_text": q.question_text,
                "topic": t_name,
                "selected_answer": user_ans,
                "correct_answer": q.correct_answer,
                "is_correct": is_correct,
                "explanation": q.explanation
            })

        percentage = round((correct_count / max(total_questions, 1)) * 100, 1)

        # Classify skill level
        if percentage >= 80.0:
            assigned_level = "Advanced"
        elif percentage >= 50.0:
            assigned_level = "Intermediate"
        else:
            assigned_level = "Beginner"

        # Determine Strong and Weak Topics
        strong_topics = []
        weak_topics = []
        for t_name, stats in topic_scores.items():
            t_pct = (stats["correct"] / stats["total"]) * 100
            if t_pct >= 66.0:
                strong_topics.append(t_name)
            else:
                weak_topics.append(t_name)

        # Save Assessment Result
        res = AssessmentResult(
            user_id=user_id,
            assessment_id=assessment.id,
            total_score=correct_count,
            max_score=total_questions,
            percentage=percentage,
            skill_level_assigned=assigned_level,
            strong_topics_json=json.dumps(strong_topics),
            weak_topics_json=json.dumps(weak_topics),
            topic_breakdown_json=json.dumps(topic_scores)
        )
        db.add(res)

        # Update Student Profile Skill Level
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
        if profile:
            profile.overall_skill_level = assigned_level

        # Update Student Skills based on topic performance
        for t_name, stats in topic_scores.items():
            t_pct = (stats["correct"] / stats["total"]) * 100
            lvl = "Advanced" if t_pct >= 80 else ("Intermediate" if t_pct >= 50 else "Beginner")
            
            # Find matching skill
            skill = db.query(Skill).filter(Skill.name.ilike(f"%{t_name[:6]}%")).first()
            if skill:
                st_skill = db.query(StudentSkill).filter(
                    StudentSkill.user_id == user_id,
                    StudentSkill.skill_id == skill.id
                ).first()
                if not st_skill:
                    st_skill = StudentSkill(user_id=user_id, skill_id=skill.id)
                    db.add(st_skill)
                st_skill.current_level = lvl
                st_skill.confidence_score = round(t_pct / 100.0, 2)
                st_skill.verified_by_assessment = True

        db.commit()

        # Trigger AI Personalized Learning Path Generation automatically!
        new_path = generate_personalized_learning_path(db, user_id)
        # Update Skill Gaps automatically!
        analyze_student_skill_gaps(db, user_id)

        return jsonify({
            "message": "Assessment processed and AI Learning Path generated successfully!",
            "result": {
                "score": correct_count,
                "total_questions": total_questions,
                "percentage": percentage,
                "assigned_level": assigned_level,
                "strong_topics": strong_topics,
                "weak_topics": weak_topics,
                "topic_breakdown": topic_scores,
                "detailed_answers": detailed_answers
            },
            "generated_learning_path": new_path
        }), 201

    except Exception as e:
        db.rollback()
        logger.error(f"Error submitting assessment: {e}")
        return jsonify({"error": "Failed to submit assessment"}), 500
    finally:
        db.close()
