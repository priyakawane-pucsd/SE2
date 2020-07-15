from __future__ import print_function
import datetime
import dateutil.parser
import pickle
import os.path
import sys  
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.now() # 'Z' indicates UTC time
    now = now + datetime.timedelta(days=30)
    prev = datetime.datetime.now() - datetime.timedelta(days=365)
	
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=(prev.isoformat()+'Z'), timeMax=(now.isoformat() + 'Z'),
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items',[])
    #print("*****",events)

    events = json.dumps(events)
    events = json.loads(events)	
    mainArray= []
    
    def calculate_days(start,end):
        d1 = dateutil.parser.parse(start)
        d2 = dateutil.parser.parse(end)
        d = d2-d1
        return d.days+1

    def get_leave_type(summary):
        if( "casual" in summary): 
            return "casual"
        elif("sick" in summary):
            return "sick"
        elif("paid" in summary):
            return "paid"
        else:
            return "undefined"

    for event in events:
        for key ,value in event.items():
            #print(key,value)
            data = {}
            if(key == "summary" and "leave" in value or key == "summary" and "from" in value):
                data["start_time"] = event['start']['dateTime']
                data["status"] = event["status"]
                data["summary"] = event["summary"]
                data["leave_type"] = get_leave_type(data["summary"])
                data["end_time"] = event["end"]["dateTime"]
                val = calculate_days(data["start_time"], data["end_time"])
                data["total_leave_days"] = val
                for attende in event["attendees"]:
                    #if(attende["responseStatus"] == "needsAction"):
                     #   data["maintainer"] = attende["email"]
                    if(attende["responseStatus"] == "accepted"):
                        data["creater"] = attende["email"]
                        data["responseStatus"] = attende["responseStatus"]

				   
                mainArray.append(data)

    fp = open("data.json","w")
    fp.write(json.dumps(mainArray, indent=4))
	


   
         

     
    '''for event in events:
        data = {}
        for attende in event["attendees"]:
            if(attende["responseStatus"] == "needsAction"):
                 data["maintainer"] = attende["email"]
            elif(attende["responseStatus"] == "accepted"):
                data["creater"] = attende["email"]
                data["responseStatus"] = attende["responseStatus"]

        data["start_time"] = event['start']['dateTime']
        data["status"] = event["status"]
        #data["summary"] = event["summary"]
        data["end_time"] = event["end"]["dateTime"]
        mainArray.append(data)'''
    #print(mainArray)


    #fp = open("data.json","w")
    #fp.write(json.dumps(mainArray, indent=4))
	
    #print(displayName)

    '''for ev in events_result['items']:
        print(ev['summary'])'''

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        #print(start, event['summary'])

if __name__ == '__main__':
    main()

