import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

URL_BASE = 'https://preciosmundi.com/'
continentes = ['europa', 'america', 'asia', 'africa', 'oceania']
countries_list = []

for continente in continentes:
    web_indice = requests.get(URL_BASE + continente).content
    soup_indice = BeautifulSoup(web_indice, "html.parser")
    links = soup_indice.css.select('.countries a')
    for link_country in links:
        url_country = link_country['href']
        name_country = link_country.text
        print(name_country)
        countries_list.append({'url': url_country, 'name': name_country})
    time.sleep(5)

print(countries_list)

for country in countries_list:
    web_restaurants = requests.get(
        country['url']+"precio-restaurantes").content
    soup_restaurants = BeautifulSoup(web_restaurants, "html.parser")
    rows = soup_restaurants.find("table").find_all("tr")
    bigmac_price = rows[5].find_all("td")[2].text
    print("Bigmac Price: "+bigmac_price)
    time.sleep(5)
