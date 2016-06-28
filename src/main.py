from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import dateutil.parser
from collections import Counter

flags = None
# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
CALENDAR_ID = 'gliacloud.com_i6u6hcmspmuq656cpf9i3i3crc@group.calendar.google.com'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main(year, month):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    time_min = '%s-%s-01T00:00:00+08:00' % (year, month)

    if month == 12:
        time_max = '%s-%s-01T00:00:00+08:00' % (year+1, 1)
    else:
        time_max = '%s-%s-01T00:00:00+08:00' % (year, month + 1)

    # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    eventsResult = service.events().list(
        calendarId=CALENDAR_ID, timeMin=time_min, timeMax=time_max, maxResults=250, singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')

    counter = Counter()

    for event in events:
        start = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date')))
        end = dateutil.parser.parse(event['end'].get('dateTime', event['end'].get('date')))
        duration = end - start
        # =IF(AND(HOUR(B2) < 12, HOUR(C2) > 14), (C2-B2)*24-1, (C2-B2)*24)
        if start.hour < 12 and end.hour > 14:
            correction = duration.total_seconds() / (60*60) - 1
        else:
            correction = duration.total_seconds() / (60*60)

        # print(event['summary'], '\t', correction)
        counter[event['summary']] += correction

    for v in counter:
        print(v, '\t', counter[v])

if __name__ == '__main__':
    import clime; clime.start(debug=True)
