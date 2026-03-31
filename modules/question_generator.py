import requests


# -------- DETECT PDF TYPE --------
def detect_pdf_type(text):
    text_lower = text.lower()

    keywords = ["usn", "subject code", "internal", "external", "total", "result"]

    score = sum(1 for word in keywords if word in text_lower)

    if score >= 3:
        return "marksheet"
    else:
        return "theory"


# -------- FILTER --------
def filter_questions(q_list):
    clean = []
    seen = set()

    for q in q_list:
        q = q.strip()

        if not q or "?" not in q:
            continue

        q_lower = q.lower()

        if q_lower in seen:
            continue

        seen.add(q_lower)
        clean.append(q)

    return clean


# -------- MAIN FUNCTION --------
def generate_questions(text, num_questions=15):

    pdf_type = detect_pdf_type(text)

    # ---------- MARKSHEET ----------
    if pdf_type == "marksheet":
        prompt = f"""
You are an intelligent question generator.

Analyze the document carefully.

Generate EXACTLY {num_questions} questions.

🚨 RULES:
- Questions MUST be directly from the content
- Questions MUST be UNIQUE
- Questions MUST cover DIFFERENT parts of the document
- Do NOT focus on only one section or one subject
- Automatically detect all entities (like student info, subjects, marks, results, dates, etc.)

📌 IMPORTANT:
- If multiple subjects are present, distribute questions across them
- If only one subject is present, generate all questions from it
- Adapt based on the document structure (do NOT assume fixed fields)

✅ Focus on:
• Key details
• Important values
• Different sections of the document

🚫 DO NOT:
- Assume fields that are not present
- Repeat same pattern
- Focus only on marks or only one subject

FORMAT:
1. Question?
2. Question?
...

CONTENT:
{text[:3000]}
"""
    # ---------- THEORY ----------
    else:
        prompt = f"""
You are an expert teacher.

Generate EXACTLY {num_questions} questions.

RULES:
-generates topic-based questions from the content
- Questions must be answerable from content
- No repetition
- Cover different concepts

Focus on:
    • Definitions
    • Key concepts
    • Types
    • Important terms

FORMAT:
1. Question?
2. Question?
...
continue numbering until {num_questions}.

CONTENT:
{text[:3000]}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "options": {
                    "temperature": 0.1,
                    "num_predict": 500
                },
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()["response"]

        raw_questions = result.split("\n")
        cleaned_questions = filter_questions(raw_questions)

        return "\n".join(cleaned_questions[:num_questions])

    except Exception as e:
        return f"Error generating questions: {e}"


        # jsjs
