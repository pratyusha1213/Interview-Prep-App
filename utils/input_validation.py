import enchant
import re

d = enchant.Dict("en_US")

ALLOWED_ABBREVIATIONS = {"HR", "CEO", "CTO", "CFO", "VP", "PM", "QA", "UX", "UI"}

def is_valid_job_title(title: str) -> bool:
    title = title.strip()

    if len(title) < 2:
        return False
    if not re.fullmatch(r"[A-Za-z\s\-]+", title):
        return False

    words = title.split()

    if len(title) <= 3 and title.upper() in ALLOWED_ABBREVIATIONS:
        return True

    for w in words:
        if len(w) <= 3 and w.upper() in ALLOWED_ABBREVIATIONS:
            continue
        if not d.check(w):
            return False

    return True

def is_valid_answer(answer: str) -> bool:
    words = re.findall(r'\b\w+\b', answer.lower())

    if len(answer.strip()) < 20 or not words:
        return False

    valid_count = sum(1 for w in words if d.check(w))
    ratio = valid_count / len(words)

    return ratio >= 0.6