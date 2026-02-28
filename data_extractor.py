import pandas as pd
import re
import dateparser

# Load labeled emails
df = pd.read_csv("data/labeled_emails.csv")

def extract_date(text):
    try:
        # Limit text size (avoid huge email crashes)
        text = str(text)[:1000]

        # Common date patterns
        date_patterns = [
            r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",           # 12/05/2024
            r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",           # 12-05-2024
            r"\b\d{1,2}\s+\w+\s+\d{4}\b",             # 12 December 2024
            r"\b\w+\s+\d{1,2},\s+\d{4}\b",            # December 12, 2024
            r"\b(today|tomorrow|next week|next month)\b"
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date = dateparser.parse(
                    match.group(),
                    settings={"PREFER_DATES_FROM": "future"}
                )
                if date:
                    return date.strftime("%Y-%m-%d %H:%M:%S")

        return None

    except Exception as e:
        return None


# Apply safely
df["extracted_date"] = df["email_text"].apply(extract_date)

# Save output
df.to_csv("data/emails_with_dates.csv", index=False)

print("Date extraction completed successfully!")
