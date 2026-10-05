import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    stop_words = set(stopwords.words("english"))
except Exception:
    stop_words = {"the", "is", "at", "which", "on", "and", "a", "an", "in", "to", "for", "with", "of", "or"}

def clean_text(text: str) -> str:
    """Preprocess text: lowercase, remove special characters, and strip extra whitespace."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s\+\#]", " ", text)
    tokens = text.split()
    filtered = [t for t in tokens if t not in stop_words and len(t) > 1]
    return " ".join(filtered)

def extract_keywords_tfidf(text: str, top_n: int = 6) -> list:
    """Extract top salient technical keywords using TF-IDF token weighting."""
    cleaned = clean_text(text)
    if not cleaned or len(cleaned.split()) < 2:
        return cleaned.split() if cleaned else []

    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=50)
        tfidf_matrix = vectorizer.fit_transform([cleaned])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        sorted_indices = scores.argsort()[::-1]
        top_keywords = [feature_names[i] for i in sorted_indices[:top_n] if scores[i] > 0]
        return top_keywords
    except Exception:
        return cleaned.split()[:top_n]

def parse_chatbot_intent(query: str) -> dict:
    """
    NLP Intent Classifier:
    Analyzes student message and determines intent and matched entities.
    """
    q_lower = query.lower()

    # Intent 1: Why recommended / explanation of recommendation
    if any(k in q_lower for k in ["why did you recommend", "why recommend", "why is this recommended", "reason for"]):
        # Extract entity
        entity = None
        for tech in ["python", "sql", "machine learning", "statistics", "math", "linear algebra", "deep learning", "nlp", "clustering"]:
            if tech in q_lower:
                entity = tech
                break
        return {"intent": "why_recommended", "entity": entity, "confidence": 0.92}

    # Intent 2: Next topic / what should I learn next
    if any(k in q_lower for k in ["what should i learn", "what next", "next topic", "where do i start", "what to learn"]):
        entity = None
        if "after" in q_lower:
            parts = q_lower.split("after")
            if len(parts) > 1:
                entity = parts[1].strip().split()[0]
        return {"intent": "next_topic", "entity": entity, "confidence": 0.89}

    # Intent 3: Concept Explanation
    if any(k in q_lower for k in ["explain", "what is", "how does", "tell me about", "define", "simply"]):
        entity = None
        for tech in ["machine learning", "supervised learning", "neural network", "deep learning", "nlp", "sql", "tf-idf", "clustering", "k-means", "regularization", "overfitting", "p-value"]:
            if tech in q_lower:
                entity = tech
                break
        return {"intent": "concept_explanation", "entity": entity, "confidence": 0.90}

    # Intent 4: Skill Gaps and Weak Areas
    if any(k in q_lower for k in ["weak", "gap", "struggling", "score", "performance", "improve"]):
        return {"intent": "skill_gaps", "entity": None, "confidence": 0.88}

    # Intent 5: Career Guidance
    if any(k in q_lower for k in ["career", "data scientist", "ai engineer", "job", "role", "roadmap"]):
        return {"intent": "career_guidance", "entity": None, "confidence": 0.85}

    return {"intent": "general_tutoring", "entity": None, "confidence": 0.70}
