import os
import fitz
import httpx
from groq import Groq

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


def get_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("❌ API KEY NOT FOUND")
        raise ValueError("Missing GROQ_API_KEY")

    http_client = httpx.Client(verify=False)
    return Groq(api_key=api_key, http_client=http_client)


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

        client = get_client()

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",
                    "content": "Answer briefly using the provided content only."
                },

                {
                    "role": "user",
                    "content": f"{content}\n\nQuestion: {question}"
                }

            ],

            max_tokens=120

        )

        answer = response.choices[0].message.content

        if not answer:
            return "⚠ Empty response"

        return answer

    except Exception as e:

        print(f"❌ ASK ERROR: {type(e).__name__}: {str(e)}")
        return f"⚠ Error: {type(e).__name__}: {str(e)}"


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
                    "content": f"Create 3 multiple choice questions from:\n\n{content}"
                }

            ],

            max_tokens=180

        )

        return response.choices[0].message.content

    except Exception as e:

        print(f"❌ QUIZ ERROR: {type(e).__name__}: {str(e)}")
        return f"⚠ Error: {type(e).__name__}: {str(e)}"


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
                    "content": f"Summarize briefly:\n\n{content}"
                }

            ],

            max_tokens=100

        )

        return response.choices[0].message.content

    except Exception as e:

        print(f"❌ SUMMARY ERROR: {type(e).__name__}: {str(e)}")
        return f"⚠ Error: {type(e).__name__}: {str(e)}"