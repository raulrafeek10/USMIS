import os
import fitz
from groq import Groq

gis_docs = []
dss_docs = []

# =========================
# Load PDFs
# =========================

def load_pdfs():

    folder = "static/files"

    if not os.path.exists(folder):
        print("❌ Folder not found")
        return

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            path = os.path.join(folder, file)

            try:

                doc = fitz.open(path)

                text = ""

                # خد أول صفحتين بس
                for page in doc[:2]:
                    text += page.get_text()

                # قص النص
                text = text[:2000]

                if file.lower().startswith("gis"):
                    gis_docs.append(text)

                elif file.lower().startswith("dss"):
                    dss_docs.append(text)

                print("✅ Loaded:", file)

            except Exception as e:
                print("❌ Error:", e)


load_pdfs()

# =========================
# Client
# =========================

def get_client():

    return Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

# =========================
# Ask Question
# =========================

def ask_question(question):

    try:

        if "dss" in question.lower():

            if not dss_docs:
                return "⚠ DSS not loaded"

            content = dss_docs[0]

        else:

            if not gis_docs:
                return "⚠ GIS not loaded"

            content = gis_docs[0]

        client = get_client()

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "user",
                    "content":
                    f"Answer shortly:\n\n{content}\n\nQuestion:{question}"
                }

            ],

            max_tokens=150

        )

        return response.choices[0].message.content

    except Exception as e:

        print("❌ ERROR:", e)

        return "⚠ AI temporarily unavailable."

# =========================
# Quiz
# =========================

def generate_quiz():

    try:

        if not gis_docs:
            return "⚠ GIS not loaded"

        content = gis_docs[0]

        client = get_client()

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "user",
                    "content":
                    f"Create 3 MCQ questions:\n\n{content}"
                }

            ],

            max_tokens=200

        )

        return response.choices[0].message.content

    except Exception as e:

        print("❌ ERROR:", e)

        return "⚠ Quiz error."

# =========================
# Summarize
# =========================

def summarize():

    try:

        if not gis_docs:
            return "⚠ GIS not loaded"

        content = gis_docs[0]

        client = get_client()

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "user",
                    "content":
                    f"Summarize shortly:\n\n{content}"
                }

            ],

            max_tokens=120

        )

        return response.choices[0].message.content

    except Exception as e:

        print("❌ ERROR:", e)

        return "⚠ Summary error."