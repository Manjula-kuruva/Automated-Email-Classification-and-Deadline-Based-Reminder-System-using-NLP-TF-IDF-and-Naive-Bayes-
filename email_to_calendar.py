
def is_cancellation_email(email_text):
    cancel_keywords = ["cancel", "cancelled", "canceled", "called off"]

    text = email_text.lower()

    return any(word in text for word in cancel_keywords)
sender_email = "client@example.com"

email_text = """
AI online meeting is rescheduled at next Saturday 2PM.

"""

from database import (
    create_table,
    insert_event,
    get_event_by_sender,
    delete_event_from_db
)
from calendar_service import create_event, delete_event
from classifier import process_email, extract_title
import datetime

create_table()

result = process_email(email_text)

if is_cancellation_email(email_text):

    existing = get_event_by_sender(sender_email)

    if existing:
        db_id, google_event_id = existing

        delete_event(google_event_id)
        delete_event_from_db(db_id)

        print(" Meeting cancelled. Event deleted from DB and Calendar.")
    else:
        print("No existing event found to cancel.")

elif result["is_reminder"] and result["event_date"]:

    title = extract_title(email_text)
    print("Processing reminder email. Extracted title:", title)

    #  Check for reschedule
    if "moved" in email_text.lower() or "reschedule" in email_text.lower():

        existing = get_event_by_sender(sender_email)

        if existing:
            db_id, google_event_id = existing

            delete_event(google_event_id)
            delete_event_from_db(db_id)

            print("Old event deleted based on sender email")

    # Create new event
    event_date = result["event_date"]
    end_time = event_date + datetime.timedelta(hours=1)

    google_event_id = create_event(
        summary=title,
        start_time=event_date,
        end_time=end_time
    )

    insert_event(
        sender_email=sender_email,
        event_title=title,
        start_time=event_date,
        end_time=end_time,
        google_event_id=google_event_id
    )

    print(" Event created/updated successfully.")
    #mark_as_read(email["id"])


