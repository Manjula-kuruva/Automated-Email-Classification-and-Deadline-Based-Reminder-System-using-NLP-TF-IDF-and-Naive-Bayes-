import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load processed data
df = pd.read_csv("data/processed_emails.csv")

X = df["clean_text"]
y = df["label"]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=5000)
X_tfidf = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.2, random_state=42
)

# Naive Bayes model
model = MultinomialNB(class_prior=[0.5, 0.5])
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model & vectorizer
joblib.dump(model, "models/naive_bayes_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("Model and vectorizer saved")
