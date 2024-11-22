import base64
import os.path
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
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
    return creds

def get_last_email(service):
    results = service.users().messages().list(userId='me', maxResults=1).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("No messages found.")
        return None
    else:
        msg = service.users().messages().get(userId='me', id=messages[0]['id'], format='full').execute()
        
        if 'parts' in msg['payload']:
            last_email_body = msg['payload']['parts'][0]['body']['data']
        else:
            last_email_body = msg['payload']['body']['data']

        return base64.urlsafe_b64decode(last_email_body).decode('utf-8')

def send_email(service, to, subject, body):
    message = {
        'raw': base64.urlsafe_b64encode(
            f"From: me\nTo: {to}\nSubject: {subject}\n\n{body}".encode('utf-8')
        ).decode('utf-8')
    }
    service.users().messages().send(userId='me', body=message).execute()
    print(f'Email sent to {to}')

def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    last_email_body = get_last_email(service)
    if last_email_body:
        signature = "\n\n-- \nYour Signature Here"
        new_body = signature + "\n" + last_email_body
        
        send_email(service, "avrodeepsaha@gmail.com", "Re: Last Email", new_body)

if __name__ == '__main__':
    main()
