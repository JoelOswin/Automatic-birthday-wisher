from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

def authenticate(CLIENT_FILE,SCOPES):
    '''Authenticates the user using the token.json if it exists or creates
    token using the CLIENT_FILE.json

    Arguments:  CLIENT_FILE:string, download the client file from google console
                SCOPES:list, check people api docs to find SCOPES
    Returns the authenticated credentials
    '''
    creds=None
    if os.path.exists('token.json'):
        creds=Credentials.from_authorized_user_file('token.json',SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file(CLIENT_FILE,SCOPES)
            creds=flow.run_local_server(port=0)
            with open('token.json','w',encoding='utf-8') as token:
                token.write(creds.to_json())
    return creds

def fetch_contacts(creds):
    '''Fetches google contacts with the help of the authenticated credentials
    
    Argument: authenticated credentials
    Returns: List of all contacts with fields: name,phoneNumbers,birthdays
    '''
    people_service=build('people','v1',credentials=creds)
    data=[]
    next_page_token=None
    while True:
        contacts=people_service.people().connections().list(resourceName='people/me',
                                                            personFields='names,phoneNumbers,birthdays',
                                                            pageSize=1000,
                                                            pageToken=next_page_token).execute()
        print(f"Contacts fetched: {len(contacts.get('connections'))}")
        for contact in contacts.get('connections'): data.append(contact)
        next_page_token=contacts.get('nextPageToken')
        if not next_page_token:
            break
    return data