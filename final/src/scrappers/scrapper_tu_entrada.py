from bs4 import BeautifulSoup
import requests
import json

def scrap_tu_entrada():
    url = 'https://eventos.tuentrada.com/list/events?lang=es'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    # soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting href attribute
    # Find all <li> elements
    # list_items = soup.find_all('li')

    # for item in list_items:
    #     title = item.find('h4').text
    #     date = item.find('span', class_='day').text.strip()
    #     time = item.find('span', class_='time').text.strip()

    #     print("Title:", title)
    #     print("Date:", date)
    #     print("Time:", time)
    #     print("---")

    # Find all product sections
    product_sections = soup.find_all('section', class_='product')
    product_info = {}

    # Iterate over each product section and extract information
    for product in product_sections:
        title_tag = product.find('h4', class_='accessibility-visually-hidden')
        date_tag = product.find('span', class_='day')
        time_tag = product.find('span', class_='time')
        location_tag = product.find('span', class_='location')
        image_tag = product.find('img')
        
        # Check if title tag exists
        if title_tag:
            product_info['title'] = title_tag.text.strip()
        
        # Check if date tag exists
        if date_tag:
            product_info['date'] = date_tag.text.strip()
        
        # Check if time tag exists
        if time_tag:
            product_info['time'] = time_tag.text.strip()
        
        # Check if location tag exists
        if location_tag:
            product_info['location'] = location_tag.text.strip()
        
        # Check if image tag exists
        if image_tag:
            product_info['image_url'] = image_tag['data-original']
        
        print("Product Info:", product_info)
        print()

    return product_info