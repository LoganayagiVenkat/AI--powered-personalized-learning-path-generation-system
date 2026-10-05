import os
import json
import random
import re
import logging
import requests

logger = logging.getLogger("learning_path.quiz_generator")

# Topic domain knowledge base for high-fidelity fallback generation
DOMAIN_KNOWLEDGE = {
    "python": {
        "concepts": ["List Comprehensions", "Generators & Yield", "GIL (Global Interpreter Lock)", "Decorators", "Context Managers", "Dictionary Hashing", "Virtual Environments", "Asyncio Event Loop"],
        "snippets": [
            ("squares = [x**2 for x in range(5) if x % 2 == 0]", "List comprehension filtering even squares: [0, 4, 16]"),
            ("def gen(): yield 1; yield 2", "Generator function yielding lazy state values using minimal memory"),
            ("with open('data.txt') as f: data = f.read()", "Context manager ensuring deterministic file descriptor cleanup"),
            ("@timing_decorator\ndef compute(): pass", "Higher-order function wrapping another function to inject telemetry")
        ],
        "pitfalls": ["Mutating a default list argument across multiple function calls", "Confusing shallow copy with deepcopy for nested structures", "Assuming GIL allows multi-core CPU bound speedup via threading", "Unchecked KeyError when accessing missing dict keys without .get()"],
        "best_practices": ["Use dict.get(key, default) or defaultdict to prevent KeyError", "Favor generators over massive in-memory lists for large streaming datasets", "Always close resources via 'with' context manager blocks", "Write explicit unit tests using pytest or unittest"]
    },
    "machine learning": {
        "concepts": ["Cross-Validation", "Bias-Variance Tradeoff", "Gradient Descent", "L1 / L2 Regularization", "Precision vs Recall", "ROC-AUC Score", "Feature Scaling", "Data Leakage"],
        "snippets": [
            ("from sklearn.model_selection import KFold", "K-Fold cross-validation partitioning training data to prevent optimistic leakage"),
            ("X_scaled = (X - X.mean()) / X.std()", "Standard Z-score normalization centering feature distributions"),
            ("loss = mse + lambda_val * sum(abs(w))", "L1 Lasso regularization driving non-essential coefficients to exact zero"),
            ("precision = tp / (tp + fp)", "Fraction of true positive alerts among all positively predicted instances")
        ],
        "pitfalls": ["Fitting scalers on entire dataset prior to train-test splitting (data leakage)", "Evaluating an imbalanced dataset solely on raw accuracy", "Training without regularization leading to severe overfitting", "Ignoring multicollinearity among highly correlated features"],
        "best_practices": ["Fit feature scalers exclusively on training splits before transforming validation sets", "Use PR-AUC and F1-score when evaluating highly skewed or imbalanced classes", "Apply L2 Ridge or L1 Lasso regularization to constrain model complexity", "Implement stratified k-fold cross validation for reproducible performance"]
    },
    "sql": {
        "concepts": ["B-Tree Indexing", "ACID Transactions", "Database Normalization (3NF)", "Inner vs Outer Joins", "Window Functions (ROW_NUMBER)", "Query Execution Plans", "Foreign Key Cascades", "Deadlocks"],
        "snippets": [
            ("SELECT dept_id, AVG(salary) FROM emp GROUP BY dept_id HAVING AVG(salary) > 50000;", "Aggregation with HAVING filtering groups after post-grouping calculation"),
            ("SELECT name, ROW_NUMBER() OVER(PARTITION BY dept ORDER BY score DESC) FROM rank_table;", "Analytical window function computing rank per department partition"),
            ("CREATE INDEX idx_user_email ON users(email);", "B-tree index speeding up lookup operations from O(N) scan to O(log N)"),
            ("BEGIN TRANSACTION; UPDATE accounts SET bal = bal - 100 WHERE id = 1; COMMIT;", "Atomic transaction ensuring financial state consistency under failures")
        ],
        "pitfalls": ["Running SELECT * on high-cardinality tables causing full table scans and memory exhaustion", "Omitting indexes on foreign key join columns leading to slow nested loop joins", "Using WHERE instead of HAVING for aggregated summary columns", "N+1 query anti-pattern in ORM iterations instead of joined pre-fetching"],
        "best_practices": ["Index frequently filtered and joined columns to avoid sequential disk scans", "Use parameterized queries or ORM binds to prevent SQL injection vulnerabilities", "Normalize schema to 3NF to eliminate duplicate anomalies, then denormalize selectively for read caching", "Analyze slow queries with EXPLAIN ANALYZE execution plan inspections"]
    },
    "nlp": {
        "concepts": ["TF-IDF Matrix", "Word Embeddings (Word2Vec / GloVe)", "Tokenization & Lemmatization", "Cosine Similarity", "Transformer Self-Attention", "Stopword Removal", "N-Gram Language Models", "Named Entity Recognition (NER)"],
        "snippets": [
            ("tfidf = TfidfVectorizer(ngram_range=(1,2), max_features=1000)", "Extracting unigram and bigram token matrices weighted by inverse document rarity"),
            ("similarity = dot(v1, v2) / (norm(v1) * norm(v2))", "Cosine similarity measuring angular alignment regardless of vector magnitude"),
            ("tokens = [lemmatizer.lemmatize(w) for w in doc if w not in stops]", "Standard text cleaning reducing morphological inflections to base lemma forms"),
            ("attention_weights = softmax((Q @ K.T) / sqrt(d_k))", "Scaled dot-product self-attention dynamically weighing context token relevance")
        ],
        "pitfalls": ["Stripping punctuation or negation words ('not', 'no') which reverses sentiment analysis polarity", "Treating out-of-vocabulary words as errors without fallback unknown token embeddings", "Assuming TF-IDF retains syntactic word order and sentence semantic flow", "Using Euclidean distance instead of Cosine similarity on un-normalized high dimensional text vectors"],
        "best_practices": ["Use lemmatization rather than crude stemming when grammatical correctness is critical", "Calculate Cosine Similarity for semantic document matching across differing text lengths", "Pre-train or fine-tune transformer models with contextual bidirectional embeddings", "Sanitize and lowercase training text while carefully preserving domain-specific acronyms"]
    },
    "deep learning": {
        "concepts": ["Backpropagation & Autograd", "Vanishing & Exploding Gradients", "Activation Functions (ReLU, GELU, Softmax)", "Batch Normalization", "Dropout Regularization", "Convolutional Kernels", "Learning Rate Schedulers", "Loss Landscapes"],
        "snippets": [
            ("loss.backward(); optimizer.step(); optimizer.zero_grad()", "PyTorch backpropagation computing loss gradients, updating weights, and resetting gradients"),
            ("nn.Sequential(nn.Linear(128, 64), nn.BatchNorm1d(64), nn.ReLU())", "Fully connected layer with Batch Normalization stabilizing internal covariate shifts"),
            ("nn.Dropout(p=0.3)", "Randomly deactivating 30% of neurons during training to prevent co-adaptation"),
            ("lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)", "Decaying learning rate along a cosine curve to reach smooth local minima")
        ],
        "pitfalls": ["Forgetting optimizer.zero_grad() leading to gradient accumulation across mini-batches", "Using Sigmoid in very deep feedforward networks causing vanishing gradient saturation", "Evaluating validation metrics with dropout and batchnorm still in training mode (not model.eval())", "Setting learning rate excessively high causing loss divergence (NaN)"],
        "best_practices": ["Initialize model with He/Kaiming initialization when using ReLU activations", "Always toggle model.eval() with torch.no_grad() during inference and validation passes", "Apply Gradient Clipping to stabilize recurrent or deep transformer training", "Use AdamW optimizer with cosine learning rate decay for state-of-the-art convergence"]
    }
}

def _get_matched_domain(text: str) -> dict:
    t = text.lower()
    for key, data in DOMAIN_KNOWLEDGE.items():
        if key in t:
            return data
    if any(k in t for k in ["neural", "network", "cnn", "transformer", "pytorch"]):
        return DOMAIN_KNOWLEDGE["deep learning"]
    if any(k in t for k in ["text", "language", "nlp", "speech", "token"]):
        return DOMAIN_KNOWLEDGE["nlp"]
    if any(k in t for k in ["database", "sql", "table", "query", "relational"]):
        return DOMAIN_KNOWLEDGE["sql"]
    if any(k in t for k in ["data", "model", "classification", "regression", "stat"]):
        return DOMAIN_KNOWLEDGE["machine learning"]
    return DOMAIN_KNOWLEDGE["python"]

def _call_gemini_api(prompt: str, api_key: str) -> dict | None:
    """Call Google Gemini REST API directly."""
    if not api_key:
        return None
    
    # Try gemini-1.5-flash / gemini-2.0-flash endpoint
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-pro"
    ]
    
    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2048,
                "responseMimeType": "application/json"
            }
        }
        try:
            resp = requests.post(url, json=payload, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                # Clean up any potential markdown code blocks
                text = re.sub(r"^```(?:json)?\s*", "", text.strip())
                text = re.sub(r"\s*```$", "", text.strip())
                return json.loads(text)
            else:
                logger.warning(f"Gemini {model_name} returned status {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            logger.warning(f"Error invoking Gemini API with {model_name}: {e}")
            continue

    return None

def generate_dynamic_quiz_questions(
    topic_data: dict,
    num_questions: int = 5,
    difficulty: str = "Intermediate",
    focus_type: str = "conceptual",
    api_key: str = None
) -> list:
    """
    Generate fresh, varied, high-quality multiple choice questions.
    Uses Gemini API if available, with intelligent NLP domain knowledge fallback.
    """
    topic_title = topic_data.get("title", "Curriculum Topic")
    category = topic_data.get("category", "General Technology")
    concepts = topic_data.get("concepts", [])
    description = topic_data.get("description", "")
    subtopics = topic_data.get("subtopics", [])
    
    gemini_key = api_key or os.environ.get("GEMINI_API_KEY")

    if gemini_key:
        prompt = f"""
You are an expert technical interviewer and university professor. Generate exactly {num_questions} fresh, high-quality multiple-choice questions for the following curriculum topic.

Topic: {topic_title}
Category: {category}
Target Difficulty: {difficulty}
Focus Style: {focus_type} (e.g. practical scenarios, deep concepts, code evaluation)
Key Concepts: {', '.join(concepts[:8])}
Description: {description}

Rules:
1. Every question must be clear, rigorous, and relevant to modern industry practice.
2. Provide exactly 4 options per question.
3. Only 1 option must be correct. The 3 distractors must represent realistic misconceptions, not silly nonsense.
4. Provide a thorough, educational explanation explaining why the correct option is right and the nuances involved.
5. Return JSON strictly in this format:
{{
  "questions": [
    {{
      "id": 1,
      "question_text": "...",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "..."
    }}
  ]
}}
"""
        result = _call_gemini_api(prompt, gemini_key)
        if result and "questions" in result and len(result["questions"]) > 0:
            logger.info("Successfully generated quiz questions using Gemini API")
            # Ensure proper shape
            questions = []
            for i, q in enumerate(result["questions"][:num_questions]):
                opts = list(q.get("options", []))
                corr = q.get("correct_answer")
                if corr not in opts:
                    opts[0] = corr
                random.shuffle(opts)
                questions.append({
                    "id": i + 1,
                    "question_text": q.get("question_text"),
                    "options": opts,
                    "correct_answer": corr,
                    "explanation": q.get("explanation", f"Mastery of {topic_title} concepts.")
                })
            return questions

    # Intelligent Fallback Engine
    logger.info("Synthesizing dynamic quiz questions via Intelligent NLP Engine...")
    domain = _get_matched_domain(f"{topic_title} {category} {description}")
    combined_concepts = list(set(concepts + domain.get("concepts", [])))
    random.shuffle(combined_concepts)

    generated = []
    seen_questions = set()
    qid = 1

    # Template 1: Core Architectural Principle
    for c in combined_concepts[:2]:
        q_text = f"In professional development with {topic_title}, what is the primary role of {c}?"
        correct = f"It systematically optimizes efficiency, reliability, and modularity in {topic_title} systems."
        distractors = [
            f"It completely disables error handling and exception logging for maximum throughput.",
            f"It forces all computations to run synchronously on a single thread without memory reclamation.",
            f"It serves as a deprecated legacy syntax avoided in modern {category} architectures."
        ]
        opts = [correct] + distractors
        random.shuffle(opts)
        generated.append({
            "id": qid,
            "question_text": q_text,
            "options": opts,
            "correct_answer": correct,
            "explanation": f"{c} is a fundamental pillar of {topic_title}. Mastering it ensures robust and scalable implementations."
        })
        qid += 1
        if len(generated) >= num_questions:
            break

    # Template 2: Pitfall & Production Bug Mitigation
    pitfalls = domain.get("pitfalls", [])
    if pitfalls and len(generated) < num_questions:
        sample_pitfall = random.choice(pitfalls)
        q_text = f"Which common architectural mistake frequently compromises systems built with {topic_title}?"
        correct = sample_pitfall
        distractors = [
            "Using version control with automated continuous integration tests.",
            "Structuring modular functions with documented type annotations.",
            "Validating input parameters against strict bounds before execution."
        ]
        opts = [correct] + distractors
        random.shuffle(opts)
        generated.append({
            "id": qid,
            "question_text": q_text,
            "options": opts,
            "correct_answer": correct,
            "explanation": f"Avoiding '{sample_pitfall}' is a key difference between novice code and production-grade software."
        })
        qid += 1

    # Template 3: Code Snippet / Practical Syntax Analysis
    snippets = domain.get("snippets", [])
    if snippets and len(generated) < num_questions:
        code_str, explanation_str = random.choice(snippets)
        q_text = f"Consider the following pattern commonly utilized in {topic_title}:\n`{code_str}`\nWhat is the expected outcome or intent?"
        correct = explanation_str
        distractors = [
            "It triggers a silent runtime overflow by bypassing hardware registers.",
            "It invalidates the entire memory cache and drops database tables.",
            "It converts numerical data directly into non-standard binary without encoding."
        ]
        opts = [correct] + distractors
        random.shuffle(opts)
        generated.append({
            "id": qid,
            "question_text": q_text,
            "options": opts,
            "correct_answer": correct,
            "explanation": f"The code snippet represents standard idiomatic practice: {explanation_str}."
        })
        qid += 1

    # Template 4: Best Practice Recommendation
    best_practices = domain.get("best_practices", [])
    if best_practices and len(generated) < num_questions:
        bp = random.choice(best_practices)
        q_text = f"When architecting high-reliability systems in {category}, which practice is strongly recommended for {topic_title}?"
        correct = bp
        distractors = [
            "Hardcode credentials and API keys directly into public repositories.",
            "Ignore system warnings and disable compiler/linter strict checks.",
            "Deploy services without automated regression testing or staging environments."
        ]
        opts = [correct] + distractors
        random.shuffle(opts)
        generated.append({
            "id": qid,
            "question_text": q_text,
            "options": opts,
            "correct_answer": correct,
            "explanation": f"Industry standard recommendation: {bp}."
        })
        qid += 1

    # Template 5: Subtopic Deep Dive if available
    for st in subtopics:
        if len(generated) >= num_questions:
            break
        st_title = st.get("title", "Advanced Concept")
        q_text = f"In {topic_title}, how does mastering '{st_title}' enhance overall engineering capability?"
        correct = f"It provides deep contextual mastery of {st_title} workflows and real-world execution."
        distractors = [
            f"It restricts {topic_title} to only execute on virtual simulated environments.",
            f"It replaces all underlying mathematical logic with uncalibrated heuristic estimations.",
            f"It prevents external libraries from interfacing with the core runtime."
        ]
        opts = [correct] + distractors
        random.shuffle(opts)
        generated.append({
            "id": qid,
            "question_text": q_text,
            "options": opts,
            "correct_answer": correct,
            "explanation": f"Understanding {st_title} bridges theoretical knowledge into actionable software and analytical proficiency."
        })
        qid += 1

    # Fill remainder if still short
    while len(generated) < num_questions:
        concept_choice = random.choice(combined_concepts) if combined_concepts else topic_title
        q_text = f"What is a critical performance characteristic of {concept_choice}?"
        correct = f"It optimizes computational complexity and resource utilization when scaled."
        distractors = [
            "It increases execution latency proportionally to the exponential power of input size.",
            "It generates unmonitored memory leaks that require daily hardware reboots.",
            "It produces indeterministic output values on identical valid inputs."
        ]
        opts = [correct] + distractors
        random.shuffle(opts)
        generated.append({
            "id": qid,
            "question_text": q_text,
            "options": opts,
            "correct_answer": correct,
            "explanation": f"Efficiency and determinism are core requirements when deploying {concept_choice} in production."
        })
        qid += 1

    return generated[:num_questions]

def generate_flashcards(
    topic_data: dict,
    num_cards: int = 6,
    api_key: str = None
) -> list:
    """
    Generate interactive revision flashcards for high-yield topic study.
    Each flashcard includes front (prompt/concept), back (concise explanation & example),
    category, difficulty, and a memorable pro_tip.
    """
    topic_title = topic_data.get("title", "Curriculum Topic")
    category = topic_data.get("category", "General Technology")
    concepts = topic_data.get("concepts", [])
    description = topic_data.get("description", "")
    difficulty = topic_data.get("difficulty", "Intermediate")

    gemini_key = api_key or os.environ.get("GEMINI_API_KEY")

    if gemini_key:
        prompt = f"""
You are an expert technical tutor. Create {num_cards} high-yield revision flashcards for students preparing for tech exams or interviews.

Topic: {topic_title}
Category: {category}
Difficulty: {difficulty}
Key Concepts: {', '.join(concepts[:8])}
Description: {description}

Each flashcard must contain:
- "id": number
- "front": Clear question, architectural prompt, or "What is X and why does it matter?"
- "back": High-yield, concise explanation with real-world context or syntax.
- "category": Short subtopic or domain tag
- "difficulty": "Beginner", "Intermediate", or "Advanced"
- "pro_tip": A short mnemonic, best practice, or common interview gotcha to remember.

Return JSON strictly in this format:
{{
  "flashcards": [
    {{
      "id": 1,
      "front": "...",
      "back": "...",
      "category": "...",
      "difficulty": "...",
      "pro_tip": "..."
    }}
  ]
}}
"""
        result = _call_gemini_api(prompt, gemini_key)
        if result and "flashcards" in result and len(result["flashcards"]) > 0:
            logger.info("Successfully generated flashcards via Gemini API")
            return result["flashcards"][:num_cards]

    # Intelligent Fallback Engine
    logger.info("Synthesizing revision flashcards via Intelligent NLP Engine...")
    domain = _get_matched_domain(f"{topic_title} {category} {description}")
    combined_concepts = list(set(concepts + domain.get("concepts", [])))
    random.shuffle(combined_concepts)

    cards = []
    card_id = 1

    # 1. Concept Definition Cards
    for c in combined_concepts[:3]:
        cards.append({
            "id": card_id,
            "front": f"What is '{c}' and why is it crucial in {topic_title}?",
            "back": f"'{c}' represents a core architectural mechanism in {category}. It enables reproducible, high-performance execution by modularizing state and computational dependencies.",
            "category": category,
            "difficulty": difficulty,
            "pro_tip": f"Interviewers frequently ask for practical examples of {c} in production—always be ready to describe a realistic use-case."
        })
        card_id += 1

    # 2. Pitfall / Gotcha Card
    pitfalls = domain.get("pitfalls", [])
    if pitfalls:
        p = random.choice(pitfalls)
        cards.append({
            "id": card_id,
            "front": f"Critical Pitfall: How to identify and avoid '{p}'?",
            "back": f"This issue arises when assumptions about data or memory are violated. The solution is rigorous input validation, explicit bounds testing, and adhering to language idioms.",
            "category": "Debugging & Safety",
            "difficulty": "Advanced",
            "pro_tip": "Look out for this during code reviews—write defensive assertions to catch it before production."
        })
        card_id += 1

    # 3. Practical Syntax / Code Card
    snippets = domain.get("snippets", [])
    if snippets:
        code_str, exp_str = random.choice(snippets)
        cards.append({
            "id": card_id,
            "front": f"Syntax Spotlight:\n`{code_str}`\nWhat does this pattern achieve?",
            "back": f"{exp_str}.\nThis pattern guarantees deterministic resource lifecycle and optimal memory efficiency.",
            "category": "Code Idioms",
            "difficulty": "Intermediate",
            "pro_tip": "Prefer idiomatic standard library utilities rather than reinventing custom wheels."
        })
        card_id += 1

    # 4. Best Practice / Architecture Card
    best_practices = domain.get("best_practices", [])
    if best_practices:
        bp = random.choice(best_practices)
        cards.append({
            "id": card_id,
            "front": f"Architecture Rule of Thumb for {topic_title}:",
            "back": f"Best Practice: {bp}.\nImplementing this reduces technical debt and dramatically eases long-term maintenance.",
            "category": "Architecture",
            "difficulty": "Intermediate",
            "pro_tip": "Always measure before and after applying optimizations to verify real-world gains."
        })
        card_id += 1

    # Fill if needed
    while len(cards) < num_cards:
        c_choice = random.choice(combined_concepts) if combined_concepts else "System Architecture"
        cards.append({
            "id": card_id,
            "front": f"When would you choose {c_choice} over simpler alternatives?",
            "back": f"Choose {c_choice} when requirements demand strict scalability, concurrency tolerance, or lower latency bounds under heavy workloads.",
            "category": category,
            "difficulty": difficulty,
            "pro_tip": "In system design, there are no solutions, only trade-offs. Always articulate the trade-offs!"
        })
        card_id += 1

    return cards[:num_cards]
