import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

URL_BASE = 'https://preciosmundi.com/'
continentes = ['europa', 'america', 'asia', 'africa', 'oceania']
countries_list = []

# buscamos en la página de cada continente los links
# base de todos los países que guardaremos en countries_list

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

# recorremos la lista de URL de países
for country in countries_list:
    web_restaurants = requests.get(
        country['url']+"precio-restaurantes").content
    soup_restaurants = BeautifulSoup(web_restaurants, "html.parser")
    rows = soup_restaurants.find("table").find_all("tr")

    # si solo hay tres columas el precio viene solo en Dólar y Euro
    # por lo que el precio en dólar esta en la columna 1
    if len(rows[0].find_all("td")) == 3:
        i_dolar = 1
    # en caso contraro suponemos que el precio en dólar está en columna 2
    else:
        i_dolar = 2

    beer_price = rows[5].find_all("td")[i_dolar].find(string=True)
    bigmac_price = rows[6].find_all("td")[i_dolar].find(string=True)

    print(country['name'])
    print("Bigmac menu price: " + bigmac_price)
    print("Beer price: " + beer_price)
    time.sleep(5)
