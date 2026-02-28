import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Load data
df = pd.read_csv("data/labeled_emails.csv")

stop_words = set(stopwords.words("english"))

def clean_text(text):
    # Remove email headers (basic)
    text = re.sub(r"From:.*?\n", "", text, flags=re.DOTALL)
    text = re.sub(r"To:.*?\n", "", text, flags=re.DOTALL)
    text = re.sub(r"Subject:.*?\n", "", text, flags=re.DOTALL)

    # Lowercase
    text = text.lower()

    # Remove non-alphabet characters
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove stopwords
    words = text.split()
    words = [w for w in words if w not in stop_words]

    return " ".join(words)

df["clean_text"] = df["email_text"].apply(clean_text)

df.to_csv("data/processed_emails.csv", index=False)

print("Preprocessing completed")
