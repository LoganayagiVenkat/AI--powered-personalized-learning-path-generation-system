import logging
from sqlalchemy.orm import Session
from backend.models.models import (
    User, StudentProfile, CareerGoal, LearningPath, LearningPathTopic,
    SkillGap, QuizResult, AssessmentResult, ChatHistory, Topic
)
from backend.ai.nlp import parse_chatbot_intent, clean_text

logger = logging.getLogger("learning_path.chatbot")

EXPLANATION_KB = {
    "machine learning": (
        "Machine Learning is a subfield of Artificial Intelligence where algorithms learn patterns "
        "directly from data instead of relying on explicit rules. For instance, instead of writing "
        "thousands of rules to detect spam emails, an ML model looks at labeled historical emails, "
        "discovers which word combinations indicate spam, and predicts new messages with high accuracy."
    ),
    "supervised learning": (
        "In Supervised Learning, an algorithm is trained on data where both the inputs (features) "
        "and correct answers (labels or targets) are provided. Common examples include predicting house prices "
        "(Regression) or classifying images as cats vs dogs (Classification)."
    ),
    "neural network": (
        "A Neural Network is an interconnected web of artificial mathematical nodes (neurons) inspired by "
        "the human brain. It passes inputs through layers, applying weights, biases, and activation functions "
        "to discover non-linear patterns. Deep neural networks power computer vision, speech recognition, and modern LLMs."
    ),
    "deep learning": (
        "Deep Learning uses neural networks with multiple hidden layers (hence 'deep') to automatically extract "
        "hierarchical features directly from raw data like pixels, audio waveforms, or sentences without manual feature engineering."
    ),
    "nlp": (
        "Natural Language Processing (NLP) enables computers to understand, interpret, and generate human language. "
        "Key techniques include tokenization, TF-IDF vectorization, semantic word embeddings, and attention-based Transformer models."
    ),
    "sql": (
        "SQL (Structured Query Language) is the standard language for managing relational databases. It allows you "
        "to filter records, perform multi-table JOINs, compute window aggregations, and query large datasets efficiently."
    ),
    "tf-idf": (
        "TF-IDF (Term Frequency-Inverse Document Frequency) measures how important a word is to a document relative to a corpus. "
        "It awards high weights to terms frequent in a specific document while penalizing common words like 'the' or 'is'."
    ),
    "clustering": (
        "Clustering is an unsupervised learning technique that groups unlabeled data points together based on similarity. "
        "In education, we use K-Means clustering to discover peer student cohorts with similar paces and strengths."
    ),
    "k-means": (
        "K-Means partitions data into K distinct non-overlapping clusters by iteratively calculating centroid coordinates "
        "and reassigning each data point to its nearest centroid until convergence."
    ),
    "regularization": (
        "Regularization prevents overfitting by penalizing overly complex models with huge coefficient weights. "
        "L1 (Lasso) promotes sparsity by zeroing out irrelevant features, while L2 (Ridge) shrinks weights smoothly."
    ),
    "overfitting": (
        "Overfitting occurs when a model memorizes noise and specifics of training data rather than underlying trends, "
        "causing it to fail when presented with unseen test data. It is mitigated by cross-validation, regularization, and dropout."
    ),
    "p-value": (
        "A p-value is the probability of observing results as extreme as the sample data under the assumption that the null "
        "hypothesis is true. A p-value below 0.05 indicates statistical significance to reject the null hypothesis."
    )
}

def generate_chatbot_response(db: Session, user_id: int, user_message: str) -> dict:
    """
    Intelligent Conversational Agent connected to student state and learning database.
    """
    # 1. Fetch User Context
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    path = db.query(LearningPath).filter(LearningPath.user_id == user_id).first()
    career_goal = db.query(CareerGoal).filter(CareerGoal.id == profile.career_goal_id).first() if profile and profile.career_goal_id else None
    target_role = career_goal.target_role if career_goal else "Data Scientist"

    # Active topic and next pending topic
    active_lpt = None
    next_pending_lpt = None
    completed_topics_titles = []
    
    if path:
        lpts = db.query(LearningPathTopic).filter(LearningPathTopic.learning_path_id == path.id).order_by(LearningPathTopic.sequence_order).all()
        for item in lpts:
            if item.status in ["in_progress", "review_needed"] and not active_lpt:
                active_lpt = item
            elif item.status == "pending" and not next_pending_lpt:
                next_pending_lpt = item
            elif item.status == "completed":
                completed_topics_titles.append(item.topic.title if item.topic else "Module")

    # Parse Intent
    intent_data = parse_chatbot_intent(user_message)
    intent = intent_data["intent"]
    entity = intent_data.get("entity")

    response_text = ""
    context_topic_id = None

    # Handle Intent: Next Topic / What to learn today
    if intent == "next_topic":
        if active_lpt and active_lpt.topic:
            context_topic_id = active_lpt.topic.id
            response_text = (
                f"Based on your target goal to become a **{target_role}**, your current active focus is "
                f"**{active_lpt.topic.title}** ({active_lpt.topic.difficulty} level). "
                f"Once you complete its practice and quiz, your next recommended step is **{next_pending_lpt.topic.title if next_pending_lpt and next_pending_lpt.topic else 'Advanced Projects'}**."
            )
        elif next_pending_lpt and next_pending_lpt.topic:
            context_topic_id = next_pending_lpt.topic.id
            response_text = (
                f"Your next scheduled topic on your roadmap is **{next_pending_lpt.topic.title}**. "
                f"It is estimated to take {next_pending_lpt.estimated_learning_time}."
            )
        else:
            response_text = (
                f"For your target path as a **{target_role}**, we recommend starting with **Python Programming Fundamentals** "
                f"followed by **SQL & Relational Databases** and **Probability & Descriptive Statistics**."
            )

    # Handle Intent: Why Recommended
    elif intent == "why_recommended":
        # Check if user mentioned a specific skill/topic
        matched_lpt = None
        if entity and path:
            for lpt in path.path_topics:
                if lpt.topic and entity.lower() in lpt.topic.title.lower():
                    matched_lpt = lpt
                    break
        if not matched_lpt:
            matched_lpt = active_lpt

        if matched_lpt and matched_lpt.topic:
            context_topic_id = matched_lpt.topic.id
            response_text = (
                f"**Why {matched_lpt.topic.title} was recommended:**\n\n"
                f"• **Target Role Alignment:** Your target career '{target_role}' requires competency in {matched_lpt.topic.category}.\n"
                f"• **Prerequisite Sequence:** Our DAG sequencing engine placed this module at position #{matched_lpt.sequence_order} to ensure you have the prerequisite foundation.\n"
                f"• **AI Reasoning:** {matched_lpt.recommended_reason}"
            )
        else:
            response_text = (
                f"Topics are dynamically sequenced using our AI engine: Content-Based TF-IDF matching pairs your '{target_role}' goal "
                f"with core curriculum requirements, while DAG topological traversal ensures prerequisites are cleared in logical order."
            )

    # Handle Intent: Concept Explanation
    elif intent == "concept_explanation":
        matched_concept = None
        if entity:
            for k in EXPLANATION_KB:
                if k in entity.lower() or entity.lower() in k:
                    matched_concept = k
                    break
        if not matched_concept:
            # Search user message for known concepts
            for k in EXPLANATION_KB:
                if k in user_message.lower():
                    matched_concept = k
                    break

        if matched_concept:
            response_text = f"**{matched_concept.title()} explained simply:**\n\n{EXPLANATION_KB[matched_concept]}"
        else:
            response_text = (
                f"Here is an intuitive explanation for your query: In machine learning and software engineering, "
                f"complex workflows are decomposed into modular steps: structured data ingestion, feature transformation, "
                f"algorithmic optimization, and empirical evaluation. Would you like to see a code example or practice quiz question?"
            )

    # Handle Intent: Skill Gaps and Weak Areas
    elif intent == "skill_gaps":
        gaps = db.query(SkillGap).filter(SkillGap.user_id == user_id).all()
        critical_gaps = [g.skill.name for g in gaps if g.gap_status == "Critical" and g.skill]
        moderate_gaps = [g.skill.name for g in gaps if g.gap_status == "Moderate" and g.skill]

        if critical_gaps or moderate_gaps:
            response_text = (
                f"Here is your current skill gap summary for **{target_role}**:\n\n"
                f"• **Critical Gaps:** {', '.join(critical_gaps) if critical_gaps else 'None! Great progress.'}\n"
                f"• **Moderate Gaps:** {', '.join(moderate_gaps) if moderate_gaps else 'None'}\n\n"
                f"Your learning path has automatically prioritized these topics to bridge the gap quickly."
            )
        else:
            response_text = (
                f"You have a well-rounded foundation for **{target_role}**! Check your Skill Gap dashboard "
                f"to inspect current vs required levels across all competencies."
            )

    # Handle Intent: Career Guidance
    elif intent == "career_guidance":
        response_text = (
            f"To succeed as a **{target_role}**, industry employers look for three pillars:\n\n"
            f"1. **Core Technical Depth:** Python, SQL, and robust statistical reasoning.\n"
            f"2. **Applied ML/AI:** Supervised & unsupervised algorithms, feature engineering, and neural networks.\n"
            f"3. **Production Deployment:** Writing clean modular code, using REST APIs, and containerized serving.\n\n"
            f"Your current roadmap has been calibrated to build these competencies in sequential order."
        )

    # General Tutoring fallback
    else:
        response_text = (
            f"I'm here to support your learning journey toward **{target_role}**! "
            f"You can ask me to explain any difficult concept (e.g. 'Explain machine learning simply'), "
            f"ask about your next topic ('What should I learn next?'), or ask why a topic was scheduled ('Why did you recommend SQL?')."
        )

    # Save to Chat History
    user_chat = ChatHistory(
        user_id=user_id,
        role="student",
        message=user_message,
        context_topic_id=context_topic_id,
        intent_detected=intent
    )
    ai_chat = ChatHistory(
        user_id=user_id,
        role="assistant",
        message=response_text,
        context_topic_id=context_topic_id,
        intent_detected=intent
    )
    db.add(user_chat)
    db.add(ai_chat)
    db.commit()

    return {
        "reply": response_text,
        "intent": intent,
        "context_topic_id": context_topic_id,
        "timestamp": ai_chat.timestamp.isoformat()
    }
