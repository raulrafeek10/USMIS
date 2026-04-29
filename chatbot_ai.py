import os
import re
import fitz
from groq import Groq

gis_docs = []
dss_docs = []

# ================================
# Load PDFs (small size جدا)
# ================================

def load_pdfs():

    folder = "static/files"

    gis_docs.clear()
    dss_docs.clear()

    if not os.path.exists(folder):
        print("Folder not found:", folder)
        return

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            path = os.path.join(folder, file)

            try:

                doc = fitz.open(path)

                text = ""

                for page in doc:
                    text += page.get_text()

                # 🔥 صغير جدًا لتجنب timeout
                small_text = text[:2000]

                if file.lower().startswith("gis"):
                    gis_docs.append(small_text)

                elif file.lower().startswith("dss"):
                    dss_docs.append(small_text)

            except Exception as e:

                print("Error loading:", file)
                print(e)


load_pdfs()


# ================================
# Safe client
# ================================

def get_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:

        print("GROQ_API_KEY missing")

        return None

    return Groq(api_key=api_key)


# ================================
# Simple fallback response
# ================================

def fallback_answer():

    return "⚠ AI temporarily unavailable. Try asking about GIS or DSS."


# ================================
# Ask Question
# ================================

def ask_question(question):

    client = get_client()

    if not client:
        return fallback_answer()

    question_lower = question.lower()

    if re.search(r'\bdss\b', question_lower):

        if not dss_docs:
            return "No DSS chapters loaded."

        content = dss_docs[0]

    else:

        if not gis_docs:
            return "No GIS chapters loaded."

        content = gis_docs[0]

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content":
                    f"Answer shortly based on:\n{content}\n\nQuestion: {question}"
                }
            ],

            temperature=0.3,
            max_tokens=300

        )

        return response.choices[0].message.content

    except Exception as e:

        print("ERROR:", e)

        return fallback_answer()


# ================================
# Generate Quiz
# ================================

def generate_quiz():

    client = get_client()

    if not client:
        return fallback_answer()

    if not gis_docs:
        return "No GIS chapters loaded."

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content":
                    f"Create 3 MCQ from:\n{gis_docs[0]}"
                }
            ],

            temperature=0.5,
            max_tokens=400

        )

        return response.choices[0].message.content

    except Exception as e:

        print("ERROR:", e)

        return fallback_answer()


# ================================
# Summarize
# ================================

def summarize():

    client = get_client()

    if not client:
        return fallback_answer()

    if not gis_docs:
        return "No GIS chapters loaded."

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content":
                    f"Summarize briefly:\n{gis_docs[0]}"
                }
            ],

            temperature=0.3,
            max_tokens=300

        )

        return response.choices[0].message.content

    except Exception as e:

        print("ERROR:", e)

        return fallback_answer()