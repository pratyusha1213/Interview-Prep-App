import re
import nltk

# Download once; comment this line after running locally
nltk.download('words', quiet=True)

from nltk.corpus import words

ENGLISH_WORDS = set(words.words())
ALLOWED_ABBREVIATIONS = {"HR", "CEO", "CTO", "CFO", "VP", "PM", "QA", "UX", "UI"}

def is_english_word(word: str) -> bool:
    # Check word ignoring case
    return word.lower() in ENGLISH_WORDS

def is_valid_job_title(title: str) -> bool:
    title = title.strip()

    if len(title) < 2:
        return False
    if not re.fullmatch(r"[A-Za-z\s\-]+", title):
        return False

    words_in_title = title.split()

    if len(title) <= 3 and title.upper() in ALLOWED_ABBREVIATIONS:
        return True

    for w in words_in_title:
        if len(w) <= 3 and w.upper() in ALLOWED_ABBREVIATIONS:
            continue
        if not is_english_word(w):
            return False

    return True

def is_valid_answer(answer: str) -> bool:
    words_in_answer = re.findall(r'\b\w+\b', answer.lower())

    if len(answer.strip()) < 20 or not words_in_answer:
        return False

    valid_count = sum(1 for w in words_in_answer if is_english_word(w))
    ratio = valid_count / len(words_in_answer)

    return ratio >= 0.6
