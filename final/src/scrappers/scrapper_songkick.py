from bs4 import BeautifulSoup
import requests


def scrap_songkick():
    url = 'https://www.songkick.com/es/metro-areas/32911-argentina-buenos-aires?page=1#metro-area-calendar'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup)
    # soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the number of upcoming concerts
    upcoming_concerts_count = soup.find('h2', class_='upcoming-concerts').text.strip()
    print("Number of upcoming concerts:", upcoming_concerts_count)

    # Extract information about each concert
    concerts = soup.find_all('li', class_='event-listings-element')
    for concert in concerts:
        concert_date = concert.find('time').text.strip()
        artists = concert.find('p', class_='artists').text.strip()
        venue = concert.find('p', class_='location').text.strip().split(',')[0]
        city = concert.find('span', class_='city-name').text.strip()
        print("\nDate:", concert_date)
        print("Artists:", artists)
        print("Venue:", venue)
        print("City:", city)

scrap_songkick()