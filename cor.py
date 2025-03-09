import requests
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0'
MEETING_URL = 'https://www.cor.net/government/boards-commissions-meetings/city-council/city-council-regular-meeting-documents'

class Meeting:

    date = ''
    canceled = True
    agenda = ''

    def __init__(self, date, agenda, canceled):
        self.date = date
        self.agenda = agenda
        self.canceled = canceled

    def __str__(self):
        if self.canceled:
            return "Date: " + self.date + " | No Meeting"
        else:
            return "Date: " + self.date + " | Agenda: " + self.agenda

def get_recent():

    # Get recent meeting table row
    resp = requests.get(MEETING_URL, headers = {'User-Agent': USER_AGENT})
    bs = BeautifulSoup(resp.text, 'html.parser')
    table_rows = bs.find_all('tr', class_='govAccess-reTableOddRow-4')
    recent = table_rows[0]

    # Create meeting object with agenda if meeting not canceled
    canceled = False
    agenda = ''
    if recent.contents[3].string == "No Meeting":
        canceled = True
    else:
        agenda = recent.contents[3].a['href']

    return Meeting(recent.contents[1].string, agenda, canceled)
