import requests
from bs4 import BeautifulSoup

def scrape_indiehoy(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract concert dates and titles from the IndieHoy website
        concert_info = []
        for event in soup.find_all('div', class_='event-box'):
            date = event.find('div', class_='date').text.strip()
            title = event.find('h3', class_='title').text.strip()
            concert_info.append({'date': date, 'title': title})

        return concert_info
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    indiehoy_url = 'https://indiehoy.com/eventos/'

    indiehoy_concerts = scrape_indiehoy(indiehoy_url)
    
    # Print the extracted concert information
    for i, concert in enumerate(indiehoy_concerts, 1):
        print(f"{i}. Date: {concert['date']}, Title: {concert['title']}")