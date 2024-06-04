from bs4 import BeautifulSoup
import requests


def scrap_indihoy():
    url = 'https://indiehoy.com/eventos/'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    # soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting href attribute
    hrefs = [a['href'] for a in soup.select('#hcalendar a.url')]

    # Extracting content inside summary class
    summaries = [summary.text for summary in soup.select('#hcalendar .summary')]

    # Extracting content inside location class
    locations = [location.text for location in soup.select('#hcalendar .location')]

    # Extracting time tags
    time_tags = soup.select('#hcalendar time')
    dtstarts = [tag['datetime'] for tag in time_tags if 'dtstart' in tag['class']]
    dtends = [tag['datetime'] for tag in time_tags if 'dtend' in tag['class']]

    # Grouping each block of information
    events = list(zip(hrefs, summaries, locations, dtstarts, dtends))

    print("Events:")
    for event in events:
        print("Href:", event[0])
        print("Summary:", event[1])
        print("Location:", event[2])
        print("Dtstart:", event[3])
        print("Dtend:", event[4])
        print()