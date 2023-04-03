import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

URL_BASE = 'https://preciosmundi.com/'
continentes = ['europa', 'america', 'asia', 'africa', 'oceania']
url_countries_list = []

for continente in continentes:
    web_indice = requests.get(URL_BASE + continente).text
    soup_indice = BeautifulSoup(web_indice, "html.parser")
    links = soup_indice.css.select('.countries a')
    for link_country in links:
        print(link_country)
        url_country = link_country['href']
        url_countries_list.append(url_country)
    time.sleep(5)

print(url_countries_list)
