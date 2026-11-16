# Application Frequency Retrieval

Application Frequency Retrieval is a small Python utility for measuring how
often the word **“application”** appears in a Gmail inbox over time. It
searches Gmail through IMAP, counts matching messages by their received date,
and saves the results as a CSV file that can be used for further analysis or
visualization.

## How it works

`retrieval.py`:

1. Loads `EMAIL` and `PASSWORD` from environment variables.
2. Connects securely to Gmail's IMAP server at `imap.gmail.com`.
3. Selects the `INBOX` mailbox.
4. Searches message bodies for the word `application`.
5. Retrieves message dates in batches of 200 messages.
6. Counts matches for each calendar date.
7. Writes the sorted results to `application_email_counts.csv`.

The script counts matching emails, not every occurrence of the word within an
email. A message that contains the word multiple times contributes one count
for its date.

## Requirements

- Python 3.8 or newer
- A Gmail account with IMAP access
- A Gmail app password

Install the only third-party dependency:

```bash
python -m pip install python-dotenv
```

For Gmail accounts with two-step verification enabled, create an app password
for this script. Do not use your normal Gmail password, and do not commit
credentials to the repository.

## Configuration

Create a `.env` file in the project directory:

```dotenv
EMAIL=your-email@example.com
PASSWORD=your-gmail-app-password
```

The `.env` file is ignored by Git. Keep it private and never paste its
contents into source code, issues, or commits.

## Usage

Run the script from the project directory:

```bash
python retrieval.py
```

To choose a different output path when using the function directly:

```python
from retrieval import count_application_emails

count_application_emails(
    username="your-email@example.com",
    app_password="your-gmail-app-password",
    output_file="results/application_email_counts.csv",
)
```

The command prints progress messages and creates a CSV with this structure:

```csv
Date,Count
2024-01-15,3
2024-02-02,1
```

Dates are written in `YYYY-MM-DD` format and sorted chronologically.

## Project files

| File | Description |
| --- | --- |
| `retrieval.py` | Gmail IMAP search, date aggregation, and CSV export |
| `analysis.ipynb` | Reserved for exploratory analysis of the exported data |
| `.gitignore` | Prevents the local `.env` file from being committed |

## Notes and limitations

- Only the `INBOX` mailbox is searched.
- The search is based on the email body and uses Gmail's IMAP search term
  `BODY "application"`.
- Gmail must accept the account's IMAP login. Account policies, disabled IMAP,
  or invalid app passwords will prevent the connection.
- If no matching emails are found, the script exits without creating an output
  CSV.
- Network, login, and search failures are reported in the terminal.
- Keyword matching is approximate. The search uses Gmail's `BODY "application"` match, so it counts any message containing the word, including newsletters, job alerts, receipts and software notifications. Results measure email volume mentioning "application", not job applications directly.
- Single mailbox, INBOX only. Archived or filtered mail is not included.

## License

No license has been specified for this project yet.
