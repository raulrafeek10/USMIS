import os
import re
import fitz
from groq import Groq

# Lists لتخزين النصوص
gis_docs = []
dss_docs = []

# ================================
# تحميل ملفات PDF
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

                # تقسيم حسب المادة
                if file.lower().startswith("gis"):

                    gis_docs.append(text[:15000])
                    print("✅ GIS Loaded:", file)

                elif file.lower().startswith("dss"):

                    dss_docs.append(text[:15000])
                    print("✅ DSS Loaded:", file)

            except Exception as e:

                print("❌ Error loading:", file)
                print(e)


# تحميل الملفات عند بدء السيرفر
load_pdfs()


# ================================
# إنشاء Groq client وقت الحاجة فقط
# ================================
def get_client():

    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:

        print("❌ GROQ_API_KEY not found!")

        raise ValueError(
            "GROQ_API_KEY environment variable is missing"
        )

    return Groq(api_key=api_key)


# ================================
# سؤال AI
# ================================
def ask_question(question):

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

        client = get_client()

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

        return "⚠ AI error occurred."


# ================================
# Generate Quiz
# ================================
def generate_quiz():

    if not gis_docs:
        return "⚠ No GIS chapters loaded."

    content = "\n".join(gis_docs[:3])

    try:

        client = get_client()

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

        return "⚠ Quiz generation error."


# ================================
# Summarize
# ================================
def summarize():

    if not gis_docs:
        return "⚠ No GIS chapters loaded."

    content = "\n".join(gis_docs[:3])

    try:

        client = get_client()

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