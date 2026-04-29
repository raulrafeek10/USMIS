import os
import fitz
import requests

gis_docs = []
dss_docs = []


def load_pdfs():

    folder = "static/files"

    if not os.path.exists(folder):
        print("❌ Folder not found:", folder)
        return

    gis_docs.clear()
    dss_docs.clear()

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            path = os.path.join(folder, file)

            try:

                doc = fitz.open(path)
                text = ""

                if len(doc) > 0:
                    text = doc[0].get_text()

                text = text[:1200]

                if file.lower().startswith("gis"):
                    gis_docs.append(text)
                    print("✅ GIS Loaded:", file)

                elif file.lower().startswith("dss"):
                    dss_docs.append(text)
                    print("✅ DSS Loaded:", file)

            except Exception as e:
                print("❌ PDF ERROR:", e)


load_pdfs()


def call_ai(messages):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemma-3-4b-it:free",
            "messages": messages,
            "max_tokens": 150
        },
        timeout=30
    )

    data = response.json()
    print("🔍 OpenRouter Response:", data)

    if "choices" not in data:
        return f"⚠ OpenRouter Error: {data}"

    return data["choices"][0]["message"]["content"]


def ask_question(question):

    try:

        question_lower = question.lower()

        if "dss" in question_lower:
            if not dss_docs:
                return "⚠ DSS not loaded"
            content = dss_docs[0]
        else:
            if not gis_docs:
                return "⚠ GIS not loaded"
            content = gis_docs[0]

        messages = [
            {
                "role": "user",
                "content": f"Answer briefly using this content only:\n\n{content}\n\nQuestion: {question}"
            }
        ]

        return call_ai(messages)

    except Exception as e:
        print(f"❌ ASK ERROR: {type(e).__name__}: {str(e)}")
        return f"⚠ Error: {type(e).__name__}: {str(e)}"


def generate_quiz():

    try:

        if not gis_docs:
            return "⚠ GIS not loaded"

        content = gis_docs[0]

        messages = [
            {
                "role": "user",
                "content": f"Create 3 multiple choice questions from:\n\n{content}"
            }
        ]

        return call_ai(messages)

    except Exception as e:
        print(f"❌ QUIZ ERROR: {type(e).__name__}: {str(e)}")
        return f"⚠ Error: {type(e).__name__}: {str(e)}"


def summarize():

    try:

        if not gis_docs:
            return "⚠ GIS not loaded"

        content = gis_docs[0]

        messages = [
            {
                "role": "user",
                "content": f"Summarize briefly:\n\n{content}"
            }
        ]

        return call_ai(messages)

    except Exception as e:
        print(f"❌ SUMMARY ERROR: {type(e).__name__}: {str(e)}")
        return f"⚠ Error: {type(e).__name__}: {str(e)}"