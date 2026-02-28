import os
import pandas as pd

BASE_DIR = "data/maildir_subset"
MAX_EMAILS = 1500

emails = []
count = 0

for user in os.listdir(BASE_DIR):
    user_path = os.path.join(BASE_DIR, user)

    if not os.path.isdir(user_path):
        continue

    for root, dirs, files in os.walk(user_path):
        for file in files:
            if count >= MAX_EMAILS:
                break

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    text = f.read()
                    emails.append(text)
                    count += 1
            except Exception as e:
                # Skip files that can't be read
                continue

        if count >= MAX_EMAILS:
            break

    if count >= MAX_EMAILS:
        break

df = pd.DataFrame({"email_text": emails})
df.to_csv("data/sample_emails.csv", index=False)

print(f"Saved {count} emails safely")
