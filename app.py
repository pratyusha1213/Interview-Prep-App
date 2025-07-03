import streamlit as st
from prompts.prompt_templates import generate_prompt
from utils.gemini_api import get_gemini_response
from utils.input_validation import is_valid_job_title, is_valid_answer
from PyPDF2 import PdfReader
from docx import Document
import io
import re


def extract_text_from_resume(file) -> str:
    if file is None:
        return ""
    file_type = file.type

    if file_type == "application/pdf":
        reader = PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_type == "text/plain":
        return file.getvalue().decode("utf-8")
    return ""


def extract_questions(text):
    questions = []
    for line in text.splitlines():
        line = line.strip()
        line = re.sub(r'^\d+[\.\)]\s*', '', line)
        if line.endswith("?"):
            questions.append(line)
    return questions


def generate_questions_with_retry(prompt, temperature=0.4, max_retries=2):
    for _ in range(max_retries):
        try:
            result = get_gemini_response(prompt, temperature)
            questions = extract_questions(result)
            if len(questions) >= 10:
                return questions[:10]
        except Exception:
            continue
    return questions if questions else []


st.set_page_config(page_title="Interview Practice App", layout="centered")
st.title("AI Interview Simulator with Feedback")

with st.sidebar:
    st.header("⚙️ Settings")
    prompt_style_map = {
        "Simple": "Zero-Shot",
        "Example-Based": "Few-Shot",
        "Step-by-Step": "Chain-of-Thought",
        "Role-Playing": "Role-Based",
        "Self Review": "Self-Critique"
    }

    prompt_style_label = st.selectbox("Pick a style for the questions:", list(prompt_style_map.keys()))
    prompt_style = prompt_style_map[prompt_style_label]
    difficulty = st.selectbox("Choose how hard the questions should be:", ["Easy", "Medium", "Hard"])
    temperature = st.slider("Creativity of AI's answers (0 = straightforward, 1 = creative):", 0.0, 1.0, 0.7)
    st.markdown("---")
    st.markdown("💡 *Higher creativity means AI answers may be more imaginative but less predictable.*")
    st.markdown("---")

    if st.session_state.get("interview_started", False) and st.button("🔁 Restart Interview"):
        for key in ["interview_started", "questions", "answers", "feedback", "current_q", "waiting_for_next"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# Initialize session state
for key in ["interview_started", "questions", "answers", "feedback", "current_q", "waiting_for_next"]:
    if key not in st.session_state:
        st.session_state[key] = False if key in ("interview_started", "waiting_for_next") else 0 if key == "current_q" else []

job_title = st.text_input("Job Title:")
company_name = st.text_input("Company Name (optional):")
job_description = st.text_area("Paste the Job Description (optional):")
resume_file = st.file_uploader("Upload your Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
show_raw = st.checkbox("Show raw AI output (for debugging)")

if st.button("🎤 Start Interview") and not st.session_state.interview_started:
    if not is_valid_job_title(job_title):
        st.error("Invalid job title. Please enter a valid job title without special characters.")
    else:
        with st.spinner("Generating interview questions..."):
            full_title = f"{job_title} at {company_name}" if company_name.strip() else job_title
            resume_text = extract_text_from_resume(resume_file) if resume_file else ""
            job_desc = job_description.strip()

            prompt = f"""
You are a professional AI interview coach. Generate exactly 10 clear, relevant, and non-redundant interview questions for the role of **{full_title}**, based on the information below.

**Job Description**:
{job_desc}

**Resume**:
{resume_text}

Requirements:
- Each question must be complete, unique, and end with a question mark (?).
- Format strictly as a numbered list from 1 to 10. One line per question.
- DO NOT add any explanation or commentary.
- Ensure that the output includes exactly 10 questions. Count them carefully before finishing.
"""

            questions = generate_questions_with_retry(prompt, temperature=0.4)

            if len(questions) < 10:
                st.warning(f"Only {len(questions)} questions generated. Try modifying the inputs or style.")

            if show_raw:
                st.text_area("Raw AI output", "\n".join(questions), height=200)

            st.session_state.questions = questions
            st.session_state.answers = []
            st.session_state.feedback = []
            st.session_state.current_q = 0
            st.session_state.waiting_for_next = False
            st.session_state.interview_started = True
            st.rerun()

if st.session_state.interview_started and st.session_state.current_q < len(st.session_state.questions):
    q_idx = st.session_state.current_q
    question = st.session_state.questions[q_idx]

    st.markdown(f"### Question {q_idx + 1} of {len(st.session_state.questions)}")
    st.markdown(f"**{question}**")

    if not st.session_state.waiting_for_next:
        user_input = st.text_area("Your Answer:", key=f"answer_{q_idx}")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Submit Answer"):
                if not user_input.strip():
                    st.warning("Please enter an answer before submitting.")
                elif not is_valid_answer(user_input):
                    st.warning("Your answer seems invalid or not meaningful. Please try again.")
                else:
                    st.session_state.answers.append(user_input)
                    with st.spinner("Generating feedback..."):
                        feedback_prompt = (
                            f"You are an interview coach. Provide detailed and constructive feedback "
                            f"for this interview answer.\n\n"
                            f"**Question:** {question}\n"
                            f"**Candidate's Answer:** {user_input}\n\n"
                            f"Please keep your feedback and example answer concise and focused, ideally within 5-6 lines.\n\n"
                            f"Please provide your feedback in the following format:\n\n"
                            f"Your Answer:\n<repeat candidate's answer>\n\n"
                            f"Example (Ideal) Answer:\n<provide a concise and straight-to-the-point answer>\n\n"
                            f"Strengths:\n<list strengths of the candidate's answer>\n\n"
                            f"Weaknesses:\n<list weaknesses or areas for improvement>\n\n"
                            f"Overall Score (out of 10):\n<score>\n\n"
                            f"Focus on accuracy, clarity, completeness, and professionalism."
                        )
                        feedback = get_gemini_response(feedback_prompt, temperature=0.3)
                        st.session_state.feedback.append(feedback)
                        st.session_state.waiting_for_next = True
                        st.rerun()

        with col2:
            if st.button("Skip Question"):
                st.session_state.answers.append("[Skipped]")
                with st.spinner("Fetching example answer..."):
                    job_desc = st.session_state.get('job_desc', '').strip()
                    resume_text = st.session_state.get('resume_text', '').strip()

                    if job_desc or resume_text:
                        skip_feedback_prompt = (
                            f"You are an interview coach. The candidate skipped this question.\n\n"
                        f"**Question:** {question}\n\n"
                        f"Candidate's Resume:\n{resume_text}\n\n"
                        f"Job Description:\n{job_desc}\n\n"
                        f"Example (Ideal) Answer:\n<provide a concise and straight-to-the-point answer>\n\n"
                        f"Based on the candidate's resume and the job description, please provide a concise and focused Example (Ideal) Answer suitable for interview practice. "
                        f"Keep it brief, about 5-6 lines max."
                        )
                    else:
                        skip_feedback_prompt = (
                            f"You're an interview coach. The candidate skipped the following question:\n\n"
                            f"{question}\n\n"
                            f"Example (Ideal) Answer:\n<provide a concise and straight-to-the-point answer>\n\n"
                            f"Provide a concise and relevant ideal answer (5–6 lines max) suitable for a general interview."
                        )

                    feedback = get_gemini_response(skip_feedback_prompt, temperature=0.3)
                    st.session_state.feedback.append(feedback)
                    st.session_state.waiting_for_next = True
                    st.rerun()

    else:
        st.markdown("**Your Answer:**")
        st.markdown(st.session_state.answers[q_idx])
        st.markdown("---")
        st.markdown("**Feedback from Interview Coach:**")
        st.markdown(st.session_state.feedback[q_idx])
        if st.button("Next"):
            st.session_state.current_q += 1
            st.session_state.waiting_for_next = False
            st.rerun()

elif st.session_state.interview_started:
    st.success("🎉 Interview completed!")
    st.subheader("Your Interview Summary")
    for i, (q, a, f) in enumerate(zip(st.session_state.questions, st.session_state.answers, st.session_state.feedback), 1):
        st.markdown(f"**{i}. {q}**")
        st.markdown(f"{a}")
        st.markdown(f"{f}")
        st.markdown("---")

    if st.button("🔁 Restart Interview"):
        for key in ["interview_started", "questions", "answers", "feedback", "current_q", "waiting_for_next"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
