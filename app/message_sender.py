import pywhatkit
from datetime import date,datetime

def matched_contacts(contacts):
    final_contacts=[]
    for contact in contacts:
        temp={}
        try:
            birthdate=contact['birthdays'][0]['date']
            if date.today().month==birthdate['month']:
                if date.today().day==birthdate['day']:
                    temp['name']=contact['names'][0]['displayName']
                    temp['phoneNumber']=contact['phoneNumbers'][0]['canonicalForm']
                    final_contacts.append(temp)
        except KeyError:
            continue
    return final_contacts

def send_msg(name,phoneNumber):
    pywhatkit.sendwhatmsg(phoneNumber,
                        message=f"Happy Birthday {name}",
                        time_hour=int(datetime.now().strftime('%H')),
                        time_min=int(datetime.now().strftime('%M'))+1)