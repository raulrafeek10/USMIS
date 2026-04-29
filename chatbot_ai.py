import os
import re
import fitz
from groq import Groq

# قراءة API KEY
api_key = os.environ.get("GROQ_API_KEY")

# Debug مؤقت للتأكد
print("GROQ_API_KEY =", api_key)

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

gis_docs = []
dss_docs = []

def load_pdfs():
    folder = "static/files"
    gis_docs.clear()
    dss_docs.clear()

    if not os.path.exists(folder):
        print("❌ Folder not found")
        return

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            try:
                doc = fitz.open(path)
                text = "".join(page.get_text() for page in doc)

                if file.lower().startswith("gis"):
                    gis_docs.append(text[:15000])
                    print("✅ GIS Loaded:", file)

                elif file.lower().startswith("dss"):
                    dss_docs.append(text[:15000])
                    print("✅ DSS Loaded:", file)

            except Exception as e:
                print("❌ Error loading:", file, e)

load_pdfs()


# ===============================
# Ask Question
# ===============================

def ask_question(question):

    if not client:
        return "⚠ Chatbot not configured."

    question_lower = question.lower()

    if re.search(r'\bdss\b', question_lower):
        if not dss_docs:
            return "⚠ No DSS chapters loaded."

        content = "\n".join(dss_docs[:3])

    else:
        if not gis_docs:
            return "⚠ No GIS chapters loaded."

        content = "\n".join(gis_docs[:3])

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content":
                    f"Answer based only on this content:\n{content}\n\nQuestion: {question}"
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return "⚠ AI error."


# ===============================
# Generate Quiz
# ===============================

def generate_quiz():

    if not client:
        return "⚠ Chatbot not configured."

    if not gis_docs:
        return "⚠ No GIS chapters loaded."

    content = "\n".join(gis_docs[:3])

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content":
                    f"Create 5 multiple choice questions from:\n{content}"
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return "⚠ Quiz error."


# ===============================
# Summarize Content
# ===============================

def summarize():

    if not client:
        return "⚠ Chatbot not configured."

    if not gis_docs:
        return "⚠ No GIS chapters loaded."

    content = "\n".join(gis_docs[:3])

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content":
                    f"Summarize these chapters:\n{content}"
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return "⚠ Summary error."