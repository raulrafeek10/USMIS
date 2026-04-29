import os
import fitz
from groq import Groq

# ================================
# Lists لتخزين النصوص
# ================================

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

                # تقليل الحجم (مهم جدًا)
                text = text[:5000]

                if file.lower().startswith("gis"):

                    gis_docs.append(text)
                    print("✅ GIS Loaded:", file)

                elif file.lower().startswith("dss"):

                    dss_docs.append(text)
                    print("✅ DSS Loaded:", file)

            except Exception as e:

                print("❌ Error loading:", file)
                print(e)


# تحميل الملفات عند بدء السيرفر
load_pdfs()

# ================================
# إنشاء Client
# ================================

def get_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:

        print("❌ GROQ_API_KEY not found!")

        raise ValueError(
            "GROQ_API_KEY environment variable is missing"
        )

    return Groq(api_key=api_key)


# ================================
# Ask Question
# ================================

def ask_question(question):

    try:

        question_lower = question.lower()

        # اختيار المادة
        if "dss" in question_lower:

            if not dss_docs:
                return "⚠ DSS content not found."

            content = dss_docs[0]

        else:

            if not gis_docs:
                return "⚠ GIS content not found."

            content = gis_docs[0]

        client = get_client()

        response = client.chat.completions.create(

            # موديل خفيف وسريع
            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",
                    "content":
                    "Answer only from the given content."
                },

                {
                    "role": "user",
                    "content":
                    f"Content:\n{content}\n\nQuestion: {question}"
                }

            ],

            max_tokens=300,
            temperature=0.3

        )

        return response.choices[0].message.content

    except Exception as e:

        print("❌ ERROR ask_question:", e)

        return "⚠ AI connection error."


# ================================
# Generate Quiz
# ================================

def generate_quiz():

    try:

        if not gis_docs:
            return "⚠ GIS content not found."

        content = gis_docs[0]

        client = get_client()

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "user",
                    "content":
                    f"Create 5 MCQ questions from this content:\n\n{content}"
                }

            ],

            max_tokens=400,
            temperature=0.4

        )

        return response.choices[0].message.content

    except Exception as e:

        print("❌ ERROR generate_quiz:", e)

        return "⚠ Quiz generation error."


# ================================
# Summarize
# ================================

def summarize():

    try:

        if not gis_docs:
            return "⚠ GIS content not found."

        content = gis_docs[0]

        client = get_client()

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "user",
                    "content":
                    f"Summarize this content briefly:\n\n{content}"
                }

            ],

            max_tokens=250,
            temperature=0.3

        )

        return response.choices[0].message.content

    except Exception as e:

        print("❌ ERROR summarize:", e)

        return "⚠ Summary error."