from app.api_contacts import authenticate,fetch_contacts
from app.message_sender import matched_contacts,send_msg
import requests
import time,json

try:
    r=requests.get('https://www.google.com/')

    creds=authenticate('CLIENT_FILE.json',['https://www.googleapis.com/auth/contacts'])
    all_contacts=fetch_contacts(creds)
    contacts=matched_contacts(all_contacts)

    for contact in contacts:
        send_msg(name=contact['name'],phoneNumber=contact['phoneNumber'])
        print(f"msg sent to {contact['name']}")

except requests.exceptions.ConnectionError:
    print("No Internet, Trying after 30 seconds")
    time.sleep(30)