import os.path
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic']

def load_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Update email signature
def update_signature(service, signature):
    result = service.users().settings().sendAs().patch(
        userId='me',
        sendAsEmail='avrodeepsaha.pvt@gmail.com', 
        body={'signature': signature}
    ).execute()
    print(f"Signature updated: {result['signature']}")

def main(signature):
    creds = load_credentials()
    service = build('gmail', 'v1', credentials=creds)

    update_signature(service, signature)   

signature1 = """
<div>
    <p>Best regards,</p>
    <p><strong>Avrodeep Saha</strong><br>
    CEO<br>
    <a href="http://Example.com">aqeeq.io</a></p>
</div>
"""

signature2 = """
<div>
    <p>Cheers,</p>
    <p><strong>Avrodeep Saha</strong><br>
    Aqeeq Techs<br>
    <a href="http://example.com">aqeeq.io</a></p>
</div>
"""

main(signature1)
