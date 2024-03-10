from base64 import urlsafe_b64decode
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dateutil import parser


# Google authentication creds
CLIENT_SECRET_FILE = "client_secret_data.json" #client secret file json file
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=8000)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    return creds

service = build("gmail", "v1", credentials=authenticate())

def fetch_emails():
    read_mails = service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
    mails = read_mails.get("messages",[])
    email_list = []

    for mail in mails:

        email_message = service.users().messages().get(userId="me", id=mail["id"]).execute()

        datetime_obj = parser.parse(get_headers(email_message, "Date"))
        email_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        
        email_data = {
            "id": email_message["id"],
            "from_email": get_headers(email_message, "From"),
            "subject": get_headers(email_message, "Subject"),
            "message": get_message(email_message),
            "email_date": email_date,
            "is_read": int("UNREAD" not in email_message['labelIds'])
        }

        email_list.append(email_data)
    
    return email_list


def get_headers(email,header_name):
    headers = email.get("payload", {}).get("headers", [])
    for header in headers:
        if header["name"] == header_name:
            return header["value"]
    return None

def get_message(email):
    parts = email.get("payload",{}).get("parts", [])
    for part in parts:
        if part["mimeType"] == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                return urlsafe_b64decode(data).decode()
    return None

def mark_as_read_or_unread(email_id,action):
    if action == "read":
        mark = service.users().messages().modify(userId="me", id=email_id, body={"removeLabelIds": ["UNREAD"]}).execute()
    elif action == "unread":
        mark = service.users().messages().modify(userId="me", id=email_id, body={"addLabelIds": ["UNREAD"]}).execute()
    else:
        mark = None
    return True if mark else False

# def mark_as_unread(email_id):
#     mark = service.users().messages().modify(userId="me", id=email_id, body={"addLabelIds": ["UNREAD"]}).execute()
#     return True if mark else False

def move_to_folder(email_id,mailbox):
    move = service.users().messages().modify(userId="me", id=email_id, body={'removeLabelIds': [], 'addLabelIds': [mailbox]}).execute()
    return True if move else False