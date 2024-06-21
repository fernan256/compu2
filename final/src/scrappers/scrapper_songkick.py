from bs4 import BeautifulSoup
from datetime import datetime
import requests


def process_artists(artists):
    lines = artists.splitlines()
    if len(lines) == 2:
        processed_artists = " ".join(lines).strip()
    else:
        processed_artists = artists.strip()
    return processed_artists


def scrap_songkick():
    url = 'https://www.songkick.com/es/metro-areas/32911-argentina-buenos-aires?page=1#metro-area-calendar'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    event_list = []
    concerts = soup.find_all('li', class_='event-listings-element')
    for concert in concerts:
        concert_date = concert.find('time')
        date_string = str(concert_date).split('"')[1]


        try:
            formatted_date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%Y")
        except ValueError as e:
            if "time data" in str(e) and "%Y-%m-%dT%H:%M:%S%z" in str(e):
                try:
                    formatted_date = datetime.strptime(date_string, "%Y-%m-%d").strftime("%d/%m/%Y")
                except ValueError:
                    formatted_date = "Date not available"
            else:
                raise e

        formatted_date = datetime.strptime(formatted_date, "%d/%m/%Y")
        artist = concert.find('p', class_='artists').text.strip()
        venue = concert.find('p', class_='location').text.strip().split(',')[0]
        link = concert.find('a')['href']
        event_data = {
            'artist': artist,
            'date': formatted_date,
            'venue': venue,
            'link': f"https://www.songkick.com{link}"
        }
        event_list.append(event_data)

    return event_list
