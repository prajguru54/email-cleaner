import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email import message_from_bytes

# SCOPES: Full access to Gmail
SCOPES = ['https://mail.google.com/']

# Labels (folders) we are targeting
LABELS_TO_HANDLE = [ 'CATEGORY_PROMOTIONS']

def authenticate_gmail():
    """
    Authenticates the user with Gmail API and returns the service object.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def delete_emails(service):
    """
    Deletes all emails from specified labels (folders).
    """
    for label in LABELS_TO_HANDLE:
        print(f"\n[INFO] Searching emails in label: {label}")
        query = f"category:{label.split('_')[-1].lower()}"
        response = service.users().messages().list(userId='me', q=query).execute()
        messages = response.get('messages', [])

        if not messages:
            print(f"[INFO] No emails found in {label}.")
            continue

        print(f"[INFO] Found {len(messages)} emails in {label}. Deleting...")

        for msg in messages:
            service.users().messages().delete(userId='me', id=msg['id']).execute()
        print(f"[INFO] Deleted all emails from {label}.")

def get_folder_details(service):
    """
    Prints detailed information about emails in specified labels (folders):
    - Number of emails
    - Subjects
    - Total folder size
    - Additional helpful information
    """
    for label in LABELS_TO_HANDLE:
        print(f"\n[INFO] Gathering details for label: {label}")
        query = f"category:{label.split('_')[-1].lower()}"
        response = service.users().messages().list(userId='me', q=query, maxResults=500).execute()
        messages = response.get('messages', [])

        if not messages:
            print(f"[INFO] No emails found in {label}.")
            continue

        total_size = 0
        subjects = []
        senders = []
        
        for msg in messages:
            # Fetch full message
            msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['Subject', 'From']).execute()
            
            # Get size estimate
            total_size += int(msg_detail.get('sizeEstimate', 0))
            
            # Extract headers
            headers = msg_detail.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
            
            subjects.append(subject)
            senders.append(from_email)

        # Printing summary
        print(f"-> Total emails: {len(messages)}")
        print(f"-> Total folder size: {total_size/1024:.2f} KB ({total_size/1024/1024:.2f} MB)")
        
        print("\nSample Emails:")
        for idx, (subject, sender) in enumerate(zip(subjects[:5], senders[:5]), start=1):
            print(f"  {idx}. From: {sender} | Subject: {subject}")

        if len(messages) > 5:
            print(f"... ({len(messages) - 5} more emails not displayed)")

def main():
    """
    Main function to authenticate and perform actions.
    """
    service = authenticate_gmail()

    # Show details first
    get_folder_details(service)

    # Confirm before deleting
    confirm = input("\nDo you really want to delete all these emails? (yes/no): ").strip().lower()
    if confirm == 'yes':
        delete_emails(service)
    else:
        print("[INFO] Deletion canceled.")

if __name__ == '__main__':
    main()
