from bs4 import BeautifulSoup
import requests
import json
from . import scrapper_allaccess
from . import scrapper_tu_entrada


def scrapper(name):
    if name == 'allaccess':
        print(name)
        scrapper_allaccess.scrap_allaccess()
    elif name == 'tuentrada':
        scrapper_tu_entrada.scrap_tu_entrada()

