import streamlit as st
import time
import re
from modules.pdf_extractor import process_pdf
from modules.question_generator import generate_questions
from modules.evaluator import evaluate_all_answers
from modules.export import create_dataframe, download_csv, generate_pdf

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Quiz App", layout="wide")

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "user_answers" not in st.session_state:
    st.session_state.user_answers = []

if "results" not in st.session_state:
    st.session_state.results = None

# ---------- CSS ----------
st.markdown("""
<style>
.title {
    font-size: 70px;
    font-weight: bold;
    text-align: center;
    color: #4CAF50;
}
.section {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<p class="title">📚 AI Quiz Generator</p>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Quiz", "Results"])
st.session_state.page = page.lower()

# =========================================================
# 🏠 HOME
# =========================================================
if st.session_state.page == "home":

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.header("📂 Upload PDF")

        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

        if uploaded_file:
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())

            st.success("Uploaded successfully!")

            text = process_pdf("temp.pdf")

            if st.button("🚀 Generate Questions"):
                with st.spinner("Generating questions..."):

                    # 🔥 CLEAR OLD DATA
                    if "questions" in st.session_state:
                        for i in range(len(st.session_state.questions)):
                            key = f"answer_{i}"
                            if key in st.session_state:
                                del st.session_state[key]

                    st.session_state.user_answers = []
                    st.session_state.results = None

                    questions = generate_questions(text)

                    # 🔥 CLEAN QUESTIONS HERE
                    cleaned_questions = []
                    for q in questions.split("\n"):
                        q = q.strip()
                        q = re.sub(r"^\d+\.\s*", "", q)
                        if q:
                            cleaned_questions.append(q)

                    st.session_state.questions = cleaned_questions
                    st.session_state.text = text
                    st.session_state.start_time = time.time()
                    st.session_state.page = "quiz"

                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 📝 QUIZ
# =========================================================
elif st.session_state.page == "quiz":

    if "questions" not in st.session_state:
        st.warning("⚠️ Upload PDF first")
        st.stop()

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("📝 Quiz")

    # TIMER
    if st.session_state.start_time:
        elapsed = int(time.time() - st.session_state.start_time)
        st.info(f"⏱️ Time: {elapsed//60:02d}:{elapsed%60:02d}")

    user_answers = []
    total_q = len(st.session_state.questions)

    for i, q in enumerate(st.session_state.questions):

        default_val = ""
        if len(st.session_state.user_answers) > i:
            default_val = st.session_state.user_answers[i]

        st.markdown(f"**Q{i+1}. {q}**")

        ans = st.text_input(
            "Your Answer:",
            value=default_val,
            key=f"answer_{i}"
        )

        user_answers.append(ans)

    # AUTO SAVE
    st.session_state.user_answers = user_answers

    # PROGRESS
    answered = len([a for a in user_answers if a.strip()])
    st.progress(answered / total_q if total_q else 0)
    st.caption(f"{answered}/{total_q} answered")

    col1, col2 = st.columns(2)

    # SUBMIT
    if col1.button("📊 Submit Quiz"):
        with st.spinner("Evaluating..."):
            results = evaluate_all_answers(
                st.session_state.questions,
                st.session_state.user_answers,
                st.session_state.text
            )

            st.session_state.results = results
            st.session_state.page = "results"

        st.rerun()

    # RESET
    if col2.button("🔄 Reset Answers"):

        st.session_state.user_answers = []

        for i in range(len(st.session_state.questions)):
            key = f"answer_{i}"
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 📊 RESULTS
# =========================================================
elif st.session_state.page == "results":

    if not st.session_state.results:
        st.warning("⚠️ No results yet")
        st.stop()

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("📊 Results Dashboard")

    results = st.session_state.results

    scores = list(map(int, re.findall(r"Score:\s*(\d+)", results)))

    total_score = sum(scores)
    num_q = len(scores)
    avg_score = total_score / num_q if num_q else 0
    percentage = (total_score / (num_q * 10)) * 100 if num_q else 0

    # GRADE
    if percentage >= 90:
        grade = "A+ 🏆"
    elif percentage >= 75:
        grade = "A 🎯"
    elif percentage >= 60:
        grade = "B 👍"
    elif percentage >= 40:
        grade = "C ⚠️"
    else:
        grade = "D ❌"

    # METRICS
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📊 Total", f"{total_score}/{num_q*10}")
    col2.metric("📈 Avg", f"{avg_score:.2f}")
    col3.metric("📉 %", f"{percentage:.1f}%")
    col4.metric("🏅 Grade", grade)

    st.progress(percentage / 100)

    col1, col2 = st.columns(2)

    if col1.button("✏️ Edit Answers"):
        st.session_state.page = "quiz"
        st.rerun()

    if col2.button("🏠 Go Home"):
        st.session_state.page = "home"
        st.rerun()

    st.divider()

    st.subheader("📋 Evaluation")
    st.text_area("", results, height=300)

    df = create_dataframe(
        st.session_state.questions,
        st.session_state.user_answers,
        results
    )

    st.dataframe(df)

    col1, col2 = st.columns(2)

    col1.download_button(
        "⬇️ CSV",
        download_csv(df),
        file_name="quiz.csv",
        mime="text/csv"
    )

    pdf_bytes = generate_pdf(df)

    col2.download_button(
        "⬇️ PDF",
        pdf_bytes,
        file_name="quiz.pdf",
        mime="application/pdf"
    )

    st.markdown('</div>', unsafe_allow_html=True)