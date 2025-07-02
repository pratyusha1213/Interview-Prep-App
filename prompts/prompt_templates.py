def generate_prompt(job_title, difficulty, style):
    base_instruction = (
        f"You are an expert interviewer preparing a candidate for the role of **{job_title}**.\n"
        f"Generate exactly 10 interview questions of {difficulty} difficulty.\n"
        f"Number the questions 1 to 10.\n"
        f"Return only the questions without any explanation, introduction, or commentary.\n"
    )

    if style == "Zero-Shot":  # Simple
        return (
            base_instruction +
            "Use a direct and straightforward question format."
        )

    elif style == "Few-Shot":  # Example-Based
        return (
            "Here is an example of 2 interview questions for the role of Software Engineer (Easy):\n"
            "1. What is a variable in Python?\n"
            "2. Describe what a function is.\n\n"
            f"Now, generate exactly 10 interview questions for the role of **{job_title}** with {difficulty} difficulty.\n"
            "Number the questions 1 to 10.\n"
            "Return ONLY the questions, following the same clear and direct style as the example.\n"
            "Do NOT include any introduction or explanation."
        )

    elif style == "Chain-of-Thought":  # Step-by-Step
        return (
            "Step-by-step instructions:\n"
            f"1. Identify the key responsibilities and required skills of a {job_title}.\n"
            f"2. Generate 10 targeted interview questions that test these skills.\n\n" +
            base_instruction +
            "Ensure questions challenge the candidate’s reasoning and problem-solving."
        )

    elif style == "Role-Based":  # Role-Playing
        return (
            f"You are a senior recruiter at Google preparing interview questions for the role of **{job_title}**.\n"
            f"Generate exactly 10 challenging interview questions that a Google recruiter would ask for this position.\n"
            f"Number the questions 1 to 10.\n"
            f"Return only the list of questions without any explanation.\n"
            f"Focus on skills and responsibilities relevant to the role and use {difficulty} difficulty."
        )

    elif style == "Self-Critique":  # Self Review
        return (
            base_instruction +
            "Do NOT include any explanations, reflections, or introductions.\n"
            "Only output the numbered list of questions in a clear, direct question format."
        )

    else:
        return base_instruction
