from collections import defaultdict
from datetime import datetime
import imaplib
import os
import re
from dotenv import load_dotenv
import csv

load_dotenv()


def count_application_emails(username, app_password, output_file="application_email_counts.csv"):
  try:
    print("Connecting to Gmail IMAP server...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    print("Logging in...")
    mail.login(username, app_password)
    print("Selecting inbox...")
    mail.select("inbox")
  except Exception as e:
    print(f"\n[ERROR] Connection or login failed: {e}")
    return

  print("Searching emails for the word 'application'...")
  status, response = mail.search(None, 'BODY "application"')
  if status != "OK":
    print("Search failed.")
    mail.logout()
    return

  email_ids = response[0].split()
  if not email_ids:
    print("No matching emails found.")
    mail.logout()
    return

  print(
      f"Found {len(email_ids)} matching emails. Fetching dates in bulk (fast"
      " mode)..."
  )
  date_counts = defaultdict(int)

  # Process in batches of 200 to speed up network calls
  batch_size = 200
  for i in range(0, len(email_ids), batch_size):
    batch = email_ids[i : i + batch_size]
    id_str = b",".join(batch)

    # Fetch INTERNALDATE in bulk instead of parsing individual message headers
    status, msg_data = mail.fetch(id_str, "(INTERNALDATE)")
    if status != "OK":
      continue

    for response_part in msg_data:
      if isinstance(response_part, bytes):
        match = re.search(
            rb'INTERNALDATE "([0-9]{1,2}-[A-Za-z]{3}-[0-9]{4})', response_part
        )
        if match:
          date_str = match.group(1).decode("utf-8")
          try:
            dt = datetime.strptime(date_str, "%d-%b-%Y")
            date_key = dt.strftime("%Y-%m-%d")
            date_counts[date_key] += 1
          except Exception:
            pass

  mail.logout()

  with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Date", "Count"])
    for date, count in sorted(date_counts.items()):
      writer.writerow([date, count])

  print(f"\nDone! Results saved to {output_file}")


if __name__ == "__main__":
  EMAIL = os.getenv("EMAIL")
  PASSWORD = os.getenv("PASSWORD")
  count_application_emails(EMAIL, PASSWORD)