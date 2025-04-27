# Gmail Email Cleaner

This script helps you view and delete all emails from your Gmail account's Social and Promotions categories using the Gmail API.

## Prerequisites

- Python 3.7 or higher
- Google account

## 1. Set Up a Python Virtual Environment

It is recommended to use a virtual environment for Python projects.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## 3. Enable Gmail API and Get Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Create a new project (or select an existing one).
3. Enable the Gmail API for your project.
4. Go to **APIs & Services > Credentials**.
5. Click **Create Credentials > OAuth client ID**.
6. Select **Desktop app** as the application type.
7. Download the `credentials.json` file.
8. Place `credentials.json` in this project folder (`clear-gmails`).
9. **Important:** Go to the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) in Google Cloud Console and add your Google account email address to the "Test users" list. You must use this account to authenticate when running the script. If you do not add your email here, you will get an `access_denied` error.

> **Note:** The script will create a `token.json` file after the first successful authentication. This file stores your access token for future runs.

## 4. Running the Script

```bash
python delete_gmail_emails.py
```

- The script will show you a summary of emails in Social and Promotions.
- It will open a browser window for you to sign in and authorize access the first time.


## 5. Important Files

- `credentials.json`: Your Google OAuth credentials (downloaded from Google Cloud Console).
- `token.json`: Auto-generated after first run (stores your access token).

## 6. Safety & Notes

- **Always review the script before running.**
- Deleting emails is irreversible!
- Only emails in Social and Promotions are affected.


