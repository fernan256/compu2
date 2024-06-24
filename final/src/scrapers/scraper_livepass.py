import requests

from bs4 import BeautifulSoup
from datetime import datetime

def split_name_venue(phrase):
  parts = phrase.split("en", maxsplit=1)
  if len(parts) == 2:
    return parts[0].strip(), parts[1].strip() 
  else:
    return parts[0].strip(), None


def scrap_livepass():
    url = 'https://livepass.com.ar/t/show'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    event_list = []
    event_boxes = soup.find_all('div', class_='event-box')

    for event_box in event_boxes:
        date = event_box.get('data-date-filter', 'Date not available')
        if date != 'Date not available':
            date_obj = datetime.strptime(date, '%m/%d/%Y')
            date_obj.strftime('%d/%m/%Y')
        else:
            date_obj = 'Date not available'
        event_title = event_box.find('h1').text.strip()
        link = event_box.find('a')['href']
        artist, venue = split_name_venue(event_title)
        event_data = {
            'artist': artist,
            'date': date_obj,
            'venue': venue,
            'link': f"https://livepass.com.ar{link}"
        }
        event_list.append(event_data)

    return event_list
