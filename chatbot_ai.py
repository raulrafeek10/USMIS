import os
import fitz
from groq import Groq
import time

# ================================
# Storage
# ================================

gis_docs = []
dss_docs = []

# ================================
# Load PDFs
# ================================

def load_pdfs():

    folder = "static/files"

    gis_docs.clear()
    dss_docs.clear()

    if not os.path.exists(folder):
        print("❌ Folder not found:", folder)
        return

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            path = os.path.join(folder, file)

            try:

                doc = fitz.open(path)

                text = ""

                for page in doc:
                    text += page.get_text()

                # مهم جدًا تقليل الحجم
                text = text[:3000]

                if file.lower().startswith("gis"):

                    gis_docs.append(text)
                    print("✅ GIS Loaded:", file)

                elif file.lower().startswith("dss"):

                    dss_docs.append(text)
                    print("✅ DSS Loaded:", file)

            except Exception as e:

                print("❌ Error loading:", file)
                print(e)


# تحميل عند بدء السيرفر
load_pdfs()

# ================================
# Create Client
# ================================

def get_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY missing")

    return Groq(
        api_key=api_key,
        timeout=30
    )

# ================================
# Retry Wrapper
# ================================

def call_ai(messages):

    for attempt in range(3):

        try:

            client = get_client()

            response = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=messages,

                max_tokens=200,

                temperature=0.3

            )

            return response.choices[0].message.content

        except Exception as e:

            print(f"❌ Attempt {attempt+1} failed:", e)

            time.sleep(2)

    return "⚠ AI temporarily unavailable."


# ================================
# Ask Question
# ================================

def ask_question(question):

    try:

        question_lower = question.lower()

        if "dss" in question_lower:

            if not dss_docs:
                return "⚠ DSS content not found."

            content = dss_docs[0]

        else:

            if not gis_docs:
                return "⚠ GIS content not found."

            content = gis_docs[0]

        messages = [

            {
                "role": "system",
                "content":
                "Answer briefly using the given content."
            },

            {
                "role": "user",
                "content":
                f"Content:\n{content}\n\nQuestion:\n{question}"
            }

        ]

        return call_ai(messages)

    except Exception as e:

        print("❌ ask_question error:", e)

        return "⚠ AI connection error."


# ================================
# Generate Quiz
# ================================

def generate_quiz():

    try:

        if not gis_docs:
            return "⚠ GIS content not found."

        content = gis_docs[0]

        messages = [

            {
                "role": "user",
                "content":
                f"Create 5 MCQ questions from:\n\n{content}"
            }

        ]

        return call_ai(messages)

    except Exception as e:

        print("❌ quiz error:", e)

        return "⚠ Quiz error."


# ================================
# Summarize
# ================================

def summarize():

    try:

        if not gis_docs:
            return "⚠ GIS content not found."

        content = gis_docs[0]

        messages = [

            {
                "role": "user",
                "content":
                f"Summarize briefly:\n\n{content}"
            }

        ]

        return call_ai(messages)

    except Exception as e:

        print("❌ summarize error:", e)

        return "⚠ Summary error."