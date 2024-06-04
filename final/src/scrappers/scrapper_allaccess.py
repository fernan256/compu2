from bs4 import BeautifulSoup
import requests


def scrap_allaccess():
    url = 'https://www.allaccess.com.ar/venue/teatro-vorterix'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup)
    # soup = BeautifulSoup(html_content, 'html.parser')

    # Extract venue information
    venue_info = soup.find('div', {'class': 'venue-header'})
    venue_name = venue_info.find('h2').text.strip()
    venue_address = venue_info.find('p').text.strip()
    print("Venue Name:", venue_name)
    print("Venue Address:", venue_address)

    # Extract event information
    event_list = soup.find_all('div', {'class': 'show-thumb'})
    for event in event_list:
        event_date = event.find('h3').text.strip()
        event_title = event.find('h2').text.strip()
        print("\nEvent Date:", event_date)
        print("Event Title:", event_title)