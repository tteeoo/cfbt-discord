import requests
from bs4 import BeautifulSoup

class Meeting:
    date = ''
    canceled = True
    agenda = ''
    def __init__(self, date, agenda, canceled):
        self.date = date
        self.agenda = agenda
        self.canceled = canceled

def getMeeting(table_i=0):

    # Get recent meeting table row
    resp = requests.get('https://www.cor.net/government/boards-commissions-meetings/city-council/city-council-regular-meeting-documents',
                            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0'})
    bs = BeautifulSoup(resp.text, 'html.parser')
    table_rows = bs.find_all('tr', class_='govAccess-reTableOddRow-4')
    recent = table_rows[table_i]

    # Create meeting object with agenda if meeting not canceled
    canceled = False
    agenda = ''
    if recent.contents[3].string == 'No Meeting':
        canceled = True
    else:
        agenda = recent.contents[3].a['href']

    return Meeting(recent.contents[1].string, agenda, canceled)
