import requests

def evaluate_all_answers(questions, user_answers, context):

    qa_pairs = ""

    for i in range(len(questions)):
        if questions[i].strip():

            answer = user_answers[i].strip() if i < len(user_answers) else ""

            qa_pairs += f"""
### QUESTION {i+1}
Question:
{questions[i]}

Student Answer:
\"\"\"{answer if answer else "EMPTY"}\"\"\"

"""

    prompt = f"""
You are a STRICT university examiner.

========================
🚨 STEP-BY-STEP PROCESS (MANDATORY)
========================
For EACH question:

1. FIRST: Extract the correct answer ONLY from the CONTEXT
2. SECOND: Compare student answer with correct answer
3. THIRD: Give score based on similarity and correctness

========================
🚨 STRICT RULES
========================
- DO NOT copy student answer as correct answer
- Correct Answer MUST come from context
- If not found → write "Not found in context"

========================
📊 SCORING RULES (STRICT)
========================
- EMPTY → 0
- Completely wrong → 0–2
- Partially correct → 5–6
- Mostly correct → 7–9
- Fully correct → 10

🚨 IMPORTANT:
- If student answer is not similar → DO NOT give high marks
- Do NOT give 10 unless almost exact match

========================
📚 CONTEXT
========================
{context[:4000]}

========================
📝 QUESTIONS & ANSWERS
========================
{qa_pairs}

========================
📌 OUTPUT FORMAT
========================

### QUESTION 1
Correct Answer: <from context>
Score: <0-10>
Feedback: <compare student vs correct>

### QUESTION 2
...
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "options": {
                "temperature": 0.0,   # 🔥 VERY IMPORTANT (no randomness)
                "num_predict": 2000
            },
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
