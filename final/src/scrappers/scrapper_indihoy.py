from bs4 import BeautifulSoup
import requests
from datetime import datetime

def scrap_indihoy():
    url = 'https://indiehoy.com/eventos/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    hrefs = [a['href'] for a in soup.select('#hcalendar a.url')]
    summaries = [summary.text for summary in soup.select('#hcalendar .summary')]
    locations = [location.text for location in soup.select('#hcalendar .location')]

    time_tags = soup.select('#hcalendar time')
    dtstarts = [tag['datetime'] for tag in time_tags if 'dtstart' in tag['class']]
    dtends = [tag['datetime'] for tag in time_tags if 'dtend' in tag['class']]


    events = list(zip(hrefs, summaries, locations, dtstarts, dtends))
    event_list = []

    for event in events:
        date_list = [int(x) for x in event[3].split(", ")]
        date_obj = datetime(date_list[2], date_list[1], date_list[0])
        formatted_date = datetime.strftime(date_obj, "%d/%m/%Y")
        formatted_date = datetime.strptime(formatted_date, "%d/%m/%Y")
        event_data = {
            'artist': event[1],
            'date': formatted_date,
            'venue': event[2],
            'link': event[0]
        }
        event_list.append(event_data)

    return event_list
