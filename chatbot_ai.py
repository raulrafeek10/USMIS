import os
import re
import fitz
import requests
from datetime import datetime
from collections import Counter

# ─── DOCUMENT STORE ──────────────────────────
docs = {"gis": {}, "dss": {}, "other": {}}

# ─── QUESTION HISTORY (tracks behavior) ──────
question_history = []


# ─── LOAD PDFs ───────────────────────────────
def load_pdfs(folder="static/files"):
    if not os.path.exists(folder):
        return

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            doc = fitz.open(path)

            pages = []
            for i, page in enumerate(doc):
                text = page.get_text()
                if text.strip():
                    pages.append({"page": i + 1, "text": text})

            full_text = "".join(p["text"] for p in pages)
            entry = {"full": full_text, "pages": pages, "file": file}

            if "gis" in file.lower():
                docs["gis"][file] = entry
            elif "dss" in file.lower():
                docs["dss"][file] = entry
            else:
                docs["other"][file] = entry


load_pdfs()


# ─── SMART CONTEXT RETRIEVAL ─────────────────
def get_context(question, top_k=5, max_chars=5000):
    keywords = set(re.findall(r'\b\w{4,}\b', question.lower()))
    if not keywords:
        keywords = set(question.lower().split())

    scored = []
    for subject, files in docs.items():
        for fname, entry in files.items():
            for page in entry["pages"]:
                text_lower = page["text"].lower()
                score = sum(1 for kw in keywords if kw in text_lower)
                if score > 0:
                    scored.append({
                        "score": score,
                        "source": f"{fname} (p.{page['page']})",
                        "subject": subject,
                        "text": page["text"]
                    })

    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:top_k]

    if not top:
        all_text = ""
        for subject, files in docs.items():
            for entry in files.values():
                all_text += entry["full"][:800] + "\n"
        return all_text[:max_chars], "General content (no strong keyword match)"

    context = ""
    sources = []
    for item in top:
        chunk = item["text"][:1200]
        context += f"[Source: {item['source']} | Subject: {item['subject'].upper()}]\n{chunk}\n\n"
        sources.append(item["source"])

    return context[:max_chars], ", ".join(sources)


# ─── QUESTION BEHAVIOR ANALYZER ──────────────
def analyze_question_behavior(history: list) -> dict:
    if not history:
        return {
            "total_questions": 0,
            "subjects_asked": {},
            "repeated_topics": [],
            "confusion_signal": "No data yet",
            "engagement_level": "Unknown"
        }

    subject_count = Counter()
    topic_keywords = []

    for q in history:
        q_lower = q.lower()
        if any(w in q_lower for w in ["gis", "spatial", "map", "geographic", "location"]):
            subject_count["GIS"] += 1
        if any(w in q_lower for w in ["dss", "decision", "support", "model", "criteria"]):
            subject_count["DSS"] += 1
        if any(w in q_lower for w in ["grade", "pass", "fail", "score", "exam", "quiz", "assignment"]):
            subject_count["Grade Concerns"] += 1

        words = re.findall(r'\b\w{5,}\b', q_lower)
        topic_keywords.extend(words)

    keyword_freq = Counter(topic_keywords)
    repeated = [w for w, c in keyword_freq.most_common(5) if c >= 2]

    total = len(history)
    if total >= 10:
        engagement = "🟢 High — actively seeking help"
    elif total >= 5:
        engagement = "🟡 Medium — some engagement"
    else:
        engagement = "🔴 Low — rarely asks questions"

    confusion_signal = f"Struggling with: {', '.join(repeated[:3])}" if repeated else "No clear confusion pattern yet"

    return {
        "total_questions": total,
        "subjects_asked": dict(subject_count),
        "repeated_topics": repeated,
        "confusion_signal": confusion_signal,
        "engagement_level": engagement
    }


# ─── GRADE PREDICTOR ─────────────────────────
def predict_grade(student: dict, behavior: dict) -> dict:
    base_score = student.get("quiz_avg", 70)

    penalty = 0
    penalty += student.get("missed", 0) * 5
    penalty += student.get("late", 0) * 3
    penalty += max(0, 3 - student.get("logins", 3)) * 4

    bonus = 0
    total_q = behavior.get("total_questions", 0)
    if total_q >= 10:
        bonus = 10
    elif total_q >= 5:
        bonus = 5

    predicted = max(0, min(100, base_score - penalty + bonus))

    if predicted >= 85:
        grade_letter, verdict = "A", "Excellent — on track to pass with distinction"
    elif predicted >= 75:
        grade_letter, verdict = "B", "Good — passing comfortably"
    elif predicted >= 65:
        grade_letter, verdict = "C", "Average — passing but needs improvement"
    elif predicted >= 50:
        grade_letter, verdict = "D", "Below average — at risk of failing"
    else:
        grade_letter, verdict = "F", "High risk of failing — urgent action needed"

    return {
        "predicted_score": predicted,
        "grade_letter": grade_letter,
        "verdict": verdict,
        "base": base_score,
        "penalty": penalty,
        "bonus": bonus
    }


# ─── RISK CALCULATOR ─────────────────────────
def calculate_risk(student: dict) -> dict:
    score = 0
    breakdown = []

    missed_pts = min(student.get("missed", 0) * 10, 30)
    score += missed_pts
    breakdown.append({"factor": "Missed Assignments", "value": student.get("missed", 0), "contribution": missed_pts, "max": 30})

    inactive_pts = min(student.get("inactive", 0) * 4, 20)
    score += inactive_pts
    breakdown.append({"factor": "Inactive Days", "value": student.get("inactive", 0), "contribution": inactive_pts, "max": 20})

    logins = student.get("logins", 0)
    login_pts = 20 if logins < 3 else (10 if logins < 6 else 0)
    score += login_pts
    breakdown.append({"factor": "Low Login Frequency", "value": logins, "contribution": login_pts, "max": 20})

    late_pts = min(student.get("late", 0) * 5, 15)
    score += late_pts
    breakdown.append({"factor": "Late Submissions", "value": student.get("late", 0), "contribution": late_pts, "max": 15})

    quiz_avg = student.get("quiz_avg", 100)
    quiz_pts = 15 if quiz_avg < 60 else (7 if quiz_avg < 75 else 0)
    score += quiz_pts
    breakdown.append({"factor": "Low Quiz Average", "value": f"{quiz_avg}%", "contribution": quiz_pts, "max": 15})

    score = min(score, 100)
    level = "🔴 High Risk" if score >= 70 else ("🟡 Medium Risk" if score >= 40 else "🟢 Low Risk")

    if student.get("missed", 0) > 1 and student.get("inactive", 0) > 3:
        trajectory = "📈 Worsening"
        dropout_prob = f"{min(score + 15, 99)}%"
    elif score < 40:
        trajectory = "📉 Stable"
        dropout_prob = f"{max(score - 10, 5)}%"
    else:
        trajectory = "➡️ Stagnant"
        dropout_prob = f"{score}%"

    return {
        "score": score,
        "level": level,
        "trajectory": trajectory,
        "dropout_probability": dropout_prob,
        "breakdown": breakdown
    }


# ─── SUGGESTIONS ─────────────────────────────
def generate_suggestions(student: dict, prediction: dict, grade_pred: dict, behavior: dict) -> list:
    tips = []

    if student.get("missed", 0) > 0:
        tips.append(f"📌 Submit your {student['missed']} missing assignment(s) — raises predicted grade directly")

    if student.get("inactive", 0) > 2:
        tips.append(f"🔄 Inactive for {student['inactive']} days — even 15 mins of review today helps")

    if student.get("logins", 10) < 3:
        tips.append("📅 Log in at least 3x per week — consistency is the #1 predictor of passing")

    if student.get("late", 0) > 0:
        tips.append(f"⏰ {student['late']} late submission(s) — contact your instructor now")

    if student.get("quiz_avg", 100) < 75:
        tips.append(f"📚 Quiz average {student.get('quiz_avg')}% — review your repeated confusion topics")

    if behavior.get("repeated_topics"):
        topics = ", ".join(behavior["repeated_topics"][:3])
        tips.append(f"🔁 You keep asking about: {topics} — dedicate focused time to these")

    if grade_pred["grade_letter"] in ["D", "F"]:
        tips.append("🚨 Predicted grade is critical — book an academic advisor session this week")

    if not tips:
        tips.append("✅ Keep it up — your engagement looks solid!")

    return tips


# ─── AI CALL ─────────────────────────────────
def call_ai(messages):
    key = os.getenv("GROQ_API_KEY")
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.5
        }
    )
    return res.json()["choices"][0]["message"]["content"]


# ─── FORMAT BREAKDOWN ─────────────────────────
def format_breakdown(breakdown: list) -> str:
    lines = ["📊 Risk Factor Breakdown:", f"{'Factor':<25} {'Value':<10} {'Points':<10} {'Max'}"]
    lines.append("-" * 55)
    for b in breakdown:
        lines.append(f"{b['factor']:<25} {str(b['value']):<10} {b['contribution']:<10} {b['max']}")
    return "\n".join(lines)


# ─── MAIN ─────────────────────────────────────
def ask_question(question: str, student: dict = None) -> str:

    if student is None:
        student = {
            "missed": 2,
            "inactive": 4,
            "logins": 2,
            "late": 1,
            "quiz_avg": 58,
        }

    question_history.append(question)

    prediction  = calculate_risk(student)
    behavior    = analyze_question_behavior(question_history)
    grade_pred  = predict_grade(student, behavior)
    tips        = generate_suggestions(student, prediction, grade_pred, behavior)
    context, sources = get_context(question)

    messages = [
        {
            "role": "system",
            "content": """
You are an intelligent LMS assistant helping students with course content and academic performance.

ALWAYS respond in this exact structure:

1) 📖 Answer:
- Answer using ALL provided lecture content sources (GIS, DSS, etc.)
- Be thorough — cover all subjects mentioned in the sources
- Cite which document/subject you used
- If question is about grades/performance, skip to section 2 and 3

2) 🔮 Prediction:
- Analyze the full behavioral profile
- Comment on question patterns (what topics they keep asking about = confusion signals)
- Give a direct, honest grade trajectory assessment
- Reference predicted grade and dropout probability

3) 💡 Action Plan:
- 3-5 specific, personalized, prioritized steps
- Be encouraging but realistic

Be direct, specific, and data-driven. Never be vague.
"""
        },
        {
            "role": "user",
            "content": f"""
Lecture Content (from: {sources}):
{context}

Student Behavior:
- Missed Assignments : {student['missed']}
- Inactive Days      : {student['inactive']}
- Logins This Week   : {student['logins']}
- Late Submissions   : {student.get('late', 0)}
- Quiz Average       : {student.get('quiz_avg', 'N/A')}%

Question History Analysis:
- Total Questions Asked  : {behavior['total_questions']}
- Subjects Explored      : {behavior['subjects_asked']}
- Repeated/Confused On   : {behavior['repeated_topics']}
- Engagement Level       : {behavior['engagement_level']}

Grade Prediction:
- Predicted Score  : {grade_pred['predicted_score']}/100
- Predicted Grade  : {grade_pred['grade_letter']}
- Verdict          : {grade_pred['verdict']}
- Breakdown        : {grade_pred['base']} (quiz) - {grade_pred['penalty']} (penalties) + {grade_pred['bonus']} (engagement bonus)

Risk Profile:
- Risk Score         : {prediction['score']}/100 — {prediction['level']}
- Trajectory         : {prediction['trajectory']}
- Dropout Probability: {prediction['dropout_probability']}

Question: {question}
"""
        }
    ]

    ai_response      = call_ai(messages)
    breakdown_table  = format_breakdown(prediction["breakdown"])
    tips_text        = "\n".join(f"  {t}" for t in tips)

    return f"""
{ai_response}

{'='*60}
{breakdown_table}

🎓 Grade Prediction:
  Predicted Score : {grade_pred['predicted_score']}/100
  Predicted Grade : {grade_pred['grade_letter']}
  Verdict         : {grade_pred['verdict']}
  Calculation     : {grade_pred['base']} (quiz avg) - {grade_pred['penalty']} (penalties) + {grade_pred['bonus']} (engagement bonus)

📈 Behavioral Profile:
  Questions Asked   : {behavior['total_questions']}
  Subjects Explored : {behavior['subjects_asked']}
  Confusion Signals : {behavior['confusion_signal']}
  Engagement Level  : {behavior['engagement_level']}

🎯 Risk Score   : {prediction['score']}/100 — {prediction['level']}
📈 Trajectory   : {prediction['trajectory']}
⚠️  Dropout Risk : {prediction['dropout_probability']}

🛠️  Your Action Plan:
{tips_text}

🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}
{'='*60}
"""