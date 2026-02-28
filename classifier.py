
import joblib
import datetime
from dateparser.search import search_dates

# Load saved model and vectorizer
model = joblib.load("models/naive_bayes_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


def extract_date(text):
    try:
        results = search_dates(
            text,
            settings={"PREFER_DATES_FROM": "future"}
        )

        if not results:
            return None

        cleaned_results = []

        for match_text, date in results:

            # If time not mentioned → default 9 AM
            if not any(t in match_text.lower() for t in ["am", "pm", ":", "at"]):
                date = date.replace(hour=9, minute=0, second=0, microsecond=0)

            cleaned_results.append((match_text, date))

        return cleaned_results

    except Exception:
        return None


def process_email(email_text):
    """
    This function:
    1. Predicts if email is reminder
    2. Extracts date
    3. Returns structured result
    """

    X = vectorizer.transform([email_text])
    prediction = model.predict(X)[0]

    if prediction != 1:
        return {
            "is_reminder": False,
            "event_date": None
        }

    results = extract_date(email_text)

    if not results:
        return {
            "is_reminder": True,
            "event_date": None
        }

    # Take LAST date (important for reschedules)
    _, event_date = results[-1]

    return {
        "is_reminder": True,
        "event_date": event_date
    }
def extract_title(email_text):
    text = email_text.lower()

    # Remove reschedule words
    for word in ["is moved to", "moved to", "rescheduled to"]:
        if word in text:
            text = text.split(word)[0]

    # Remove time words
    text = text.split(" at ")[0]

    return text.strip().title()

