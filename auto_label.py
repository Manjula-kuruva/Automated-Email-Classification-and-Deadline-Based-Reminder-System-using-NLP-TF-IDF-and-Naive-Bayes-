import pandas as pd
import re

# Load email CSV
df = pd.read_csv("data/sample_emails.csv")

# Keywords indicating meetings / deadlines
KEYWORDS = [
    "meeting", "deadline", "due date", "schedule",
    "appointment", "call", "conference", "reminder",
    "submit", "presentation"
]

# Simple date patterns
DATE_PATTERN = r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b"

def is_reminder_email(text):
    text_lower = text.lower()

    # keyword match
    for kw in KEYWORDS:
        if kw in text_lower:
            return 1

    # date match
    if re.search(DATE_PATTERN, text_lower):
        return 1

    return 0

df["label"] = df["email_text"].apply(is_reminder_email)

df.to_csv("data/labeled_emails.csv", index=False)

print("Auto-labeling completed")
print(df["label"].value_counts())
