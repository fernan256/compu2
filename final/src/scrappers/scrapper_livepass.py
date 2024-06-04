from bs4 import BeautifulSoup
import requests


def scrap_livepass():
    url = 'https://livepass.com.ar/t/show'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    # soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting href attribute
    # events = soup.find_all('div', class_='event-box')

    # for event in events:
    #     date = event['data-date-filter']
    #     event_title = event.find('h1').text.strip()
    #     link = event.find('a')['href']
    #     print("Date:", date)
    #     print("Event Title:", event_title)
    #     print("Link:", link)
    #     print()

    event_boxes = soup.find_all('div', class_='event-box')

    for event_box in event_boxes:
        date = event_box.get('data-date-filter', 'Date not available')
        event_title = event_box.find('h1').text.strip()
        link = event_box.find('a')['href']
        print("Date:", date)
        print("Event Title:", event_title)
        print("Link:", link)
        print()