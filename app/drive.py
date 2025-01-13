from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv


SCOPES = ['https://www.googleapis.com/auth/drive']

load_dotenv()

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {"installed":
                    {"client_id": os.getenv('CLIENT_ID'),
                    "project_id": os.getenv('PROJECT_ID'),
                    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                    "token_uri":"https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": os.getenv('CLIENT_SECRET'),
                    "redirect_uris":["http://localhost"]}
                }
                , SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_drive_service():
    creds = get_credentials()
    return build('drive', 'v3', credentials=creds)


def list_files():
    service = get_drive_service()
    results = service.files().list(
        pageSize=1000,
        fields="files(id, name, mimeType, owners(emailAddress), shared, modifiedTime)"
    ).execute()
    return results.get('files', [])


def change_visibility(file_id):
    service = get_drive_service()
    try:
        service.permissions().delete(fileId=file_id, permissionId='anyoneWithLink').execute()
    except HttpError as error:
        print(f"An error occurred: {error}")


def get_authenticated_user_email():
    service = get_drive_service()
    about = service.about().get(fields='user').execute()
    return about['user']['emailAddress']
