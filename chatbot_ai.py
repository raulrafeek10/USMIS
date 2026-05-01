import os
import fitz
import requests

gis_docs = {}
dss_docs = {}


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

                for page in doc:
                    text += page.get_text()

                text = text[:4000]

                if file.lower().startswith("gis"):
                    num = ''.join(filter(str.isdigit, file))
                    if num:
                        gis_docs[int(num)] = text
                        print("✅ GIS Loaded:", file)

                elif file.lower().startswith("dss"):
                    num = ''.join(filter(str.isdigit, file))
                    if num:
                        dss_docs[int(num)] = text
                        print("✅ DSS Loaded:", file)

            except Exception as e:
                print("❌ PDF ERROR:", e)


load_pdfs()


def get_content(question_lower):

    chapter_num = None
    for word in question_lower.split():
        if word.isdigit():
            chapter_num = int(word)
            break

    if "dss" in question_lower:
        if chapter_num and chapter_num in dss_docs:
            return dss_docs[chapter_num]
        elif dss_docs:
            return dss_docs[min(dss_docs.keys())]
        else:
            return None
    else:
        if chapter_num and chapter_num in gis_docs:
            return gis_docs[chapter_num]
        elif gis_docs:
            return gis_docs[min(gis_docs.keys())]
        else:
            return None


def call_ai(messages):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY")

    models = [
        "google/gemma-3-4b-it:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "qwen/qwen-2.5-7b-instruct:free"
    ]

    for model in models:

        try:

            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 300
                },
                timeout=30
            )

            data = response.json()
            print(f"🔍 Model: {model} | Response: {data}")

            if "choices" in data:
                return data["choices"][0]["message"]["content"]

            print(f"⚠ Model {model} failed, trying next...")

        except Exception as e:
            print(f"❌ Model {model} error: {str(e)}")
            continue

    return "⚠ All models unavailable, please try again later."


def ask_question(question):

    try:

        question_lower = question.lower()
        content = get_content(question_lower)

        if not content:
            return "⚠ No content loaded"

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


def generate_quiz(question=""):

    try:

        question_lower = question.lower() if question else "gis"
        content = get_content(question_lower)

        if not content:
            if gis_docs:
                content = gis_docs[min(gis_docs.keys())]
            else:
                return "⚠ No content loaded"

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


def summarize(question=""):

    try:

        question_lower = question.lower() if question else "gis"
        content = get_content(question_lower)

        if not content:
            if gis_docs:
                content = gis_docs[min(gis_docs.keys())]
            else:
                return "⚠ No content loaded"

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