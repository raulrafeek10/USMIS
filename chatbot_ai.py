import os
import re
import fitz
from groq import Groq

# ================================
# تخزين النصوص
# ================================

gis_docs = []
dss_docs = []

# ================================
# تحميل PDF
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

                if file.lower().startswith("gis"):

                    gis_docs.append(text[:15000])
                    print("✅ GIS Loaded:", file)

                elif file.lower().startswith("dss"):

                    dss_docs.append(text[:15000])
                    print("✅ DSS Loaded:", file)

            except Exception as e:

                print("❌ Error loading:", file)
                print(e)


# تحميل الملفات مرة واحدة
load_pdfs()


# ================================
# إنشاء client وقت الطلب فقط
# ================================

def get_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:

        print("❌ GROQ_API_KEY missing")

        # مهم جدًا: نرجع None بدل crash
        return None

    return Groq(api_key=api_key)


# ================================
# Ask
# ================================

def ask_question(question):

    client = get_client()

    if not client:
        return "⚠ AI not configured (missing API key)"

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
                    f"Answer based only on this content:\n\n{content}\n\nQuestion: {question}"
                }
            ]

        )

        return response.choices[0].message.content

    except Exception as e:

        print("❌ ERROR:", e)

        return "⚠ AI error."


# ================================
# Quiz
# ================================

def generate_quiz():

    client = get_client()

    if not client:
        return "⚠ AI not configured"

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
                    f"Create 5 multiple choice questions from:\n\n{content}"
                }
            ]

        )

        return response.choices[0].message.content

    except Exception as e:

        print("❌ ERROR:", e)

        return "⚠ Quiz error."


# ================================
# Summary
# ================================

def summarize():

    client = get_client()

    if not client:
        return "⚠ AI not configured"

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
                    f"Summarize these chapters:\n\n{content}"
                }
            ]

        )

        return response.choices[0].message.content

    except Exception as e:

        print("❌ ERROR:", e)

        return "⚠ Summary error."