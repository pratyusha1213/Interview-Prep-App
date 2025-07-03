# AI Interview Simulator with Feedback

An interactive web app built with Streamlit that helps you practice job interviews using AI-generated questions and detailed feedback powered by an LLM API.

---

## Overview

This app simulates a job interview experience by generating tailored interview questions based on the job title, company, job description, and your resume. It allows you to answer each question and receive constructive, detailed feedback to improve your interview skills.

You can customize the style and difficulty of the questions, adjust AI creativity, and upload your resume to generate highly relevant questions.

---

## Features

* **Dynamic Interview Questions**: Generates 10 unique, role-specific interview questions using an AI API.
* **Resume & Job Description Integration**: Upload your resume (PDF, DOCX, or TXT) and paste the job description to tailor questions to your profile.
* **Prompt Styles**: Choose from various question generation techniques such as Zero-Shot, Few-Shot, Chain-of-Thought, Role-Based, and Self-Critique.
* **Difficulty Levels**: Select Easy, Medium, or Hard difficulty for generated questions.
* **Answer Submission & Feedback**: Submit your answers and get detailed, AI-generated feedback including strengths, weaknesses, example answers, and scores.
* **Skip Questions**: Option to skip questions and receive an ideal example answer for that question.
* **Adjust AI Creativity**: Use a slider to control the creativity (temperature) of AI responses.
* **Session Management**: Restart interviews at any time and track progress through questions and feedback.
* **Raw AI Output Display**: Optionally view raw AI responses for debugging or learning purposes.

---

## How It Works

1. **Input your job details**: Enter a job title, optionally a company name and job description.
2. **Upload your resume** (optional): Supports PDF, DOCX, and TXT formats.
3. **Select preferences**: Choose question style, difficulty, and AI creativity.
4. **Start the interview**: The app generates 10 interview questions tailored to your inputs.
5. **Answer questions**: Submit answers one by one and receive instant AI feedback.
6. **Review summary**: After completing all questions, review a summary of your answers and feedback.

---

## Technologies Used

* [Streamlit](https://streamlit.io/) — Web app framework for Python
* [OpenAI / Gemini API](#) — AI for question generation and feedback (via `get_gemini_response`)
* [PyPDF2](https://pypi.org/project/PyPDF2/) — Extract text from PDF resumes
* [python-docx](https://python-docx.readthedocs.io/en/latest/) — Extract text from DOCX resumes
* Regular expressions — For parsing and cleaning questions

---

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/interview-practice-app.git
   cd interview-practice-app
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables with your API keys as required.

---

## Running the App

Start the Streamlit app by running:

```bash
streamlit run app.py
```

Open your browser at the URL provided (usually `http://localhost:8501`).

---

## Code Structure

* `app.py` — Main Streamlit app with UI and interview logic
* `prompts/prompt_templates.py` — Contains prompt templates for question generation
* `utils/gemini_api.py` — Functions to interact with the Gemini/OpenAI API
* `utils/input_validation.py` — Validation functions for user inputs (job title, answers)

---

## Usage Tips

* Enter a clear job title (avoid special characters).
* Use the resume upload and job description fields to generate highly customized questions.
* Experiment with different prompt styles and difficulty levels to match your interview needs.
* Adjust the creativity slider to control how imaginative or straightforward AI responses are.
* Use the "Show raw AI output" checkbox if you want to see the raw question or feedback text.

---

## Future Improvements

* Add user authentication and saving interview sessions.
* Support multiple languages for questions and feedback.
* Implement additional AI models or APIs for varied feedback.
* Add interactive interview personas with varying difficulty and personality.

---