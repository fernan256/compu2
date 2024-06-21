from bs4 import BeautifulSoup
import requests
from datetime import datetime


def scrap_tu_entrada():
    url = 'https://eventos.tuentrada.com/list/events?lang=es'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    product_sections = soup.find_all('section', class_='product')
    event_list = []

    for product in product_sections:
        location_element = product.find('p', class_='semantic-no-styling-no-display location')
        venue = location_element.find('span', class_='site').text.strip() if location_element else None

        name_element = product.find('h4', class_='accessibility-visually-hidden')
        artist = name_element.text.strip() if name_element else None

        link_element = product.find('a', class_='product_link')
        link = link_element['href'] if link_element else None

        date_element = product.find('p', class_='semantic-no-styling-no-display date')
        date = date_element.find('span', class_='day').text.strip() if date_element else None

        formatted_date = None
        month_dict = {"enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05", "junio": "06",
              "julio": "07", "agosto": "08", "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"}
        if date:
            date_parts = date.split()[1:4]
            date_str = '/'.join(date_parts)
            date_list = [date_str.split("/")[0], month_dict[date_str.split("/")[1]], date_str.split("/")[2]]
            date_obj = datetime(int(date_list[2]), int(date_list[1]), int(date_list[0]))
            formatted_date = date_obj.strftime("%d/%m/%Y")
            formatted_date = datetime.strptime(formatted_date, "%d/%m/%Y")

        event_data = {
            'artist': artist,
            'date': formatted_date,
            'venue': venue,
            'link': f"https://eventos.tuentrada.com{link}"
        }
        event_list.append(event_data)

    return event_list
