import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import datetime

def to_csv(listaPaises, salariosMedios, preciosCerveza, preciosBigMac, nombre_archivo):
    # Crear un diccionario con los datos
    data = {'Pais': listaPaises,
            'Salario Medio': salariosMedios,
            'Cerveza': preciosCerveza,
            'Big Mac': preciosBigMac}

    # Crear un DataFrame a partir del diccionario
    dataFrame = pd.DataFrame(data)

    # Escribir la información del DataFrame en un archivo csv
    dataFrame.to_csv(nombre_archivo, index=False)

# buscamos en la página de cada continente los links
# base de todos los países que guardaremos en countries_list
def getCountriesList(continentes, URL_BASE):
    auxCountries = []
    for continente in continentes:
        web_indice = requests.get(URL_BASE + continente).content
        soup_indice = BeautifulSoup(web_indice, "html.parser")
        links = soup_indice.select('.countries a')
        for link_country in links:
            url_country = link_country['href']
            name_country = link_country.text
            print(name_country)
            auxCountries.append({'url': url_country, 'name': name_country})
    time.sleep(1)
    return auxCountries

def getSalaries(soup_restaurants):
    aside_lis = soup_restaurants.select(".container aside li")
    print(aside_lis[1])
    salary_text = aside_lis[1].getText()

    # Extraemos el salario medio
    expRegularSalarioMedio = r'\d{1,3}(?:[.,]\d{3})*(?:,\d+)'
    resultado = re.search(expRegularSalarioMedio, salary_text)
    if resultado:
        valor = resultado.group()
        print(valor)
    else:
        valor = "null"
        print(valor)
    
    return valor


URL_BASE = 'https://preciosmundi.com/'
continentes = ['europa']
# continentes = ['europa', 'america', 'asia', 'africa', 'oceania']

countries_list = getCountriesList(continentes,URL_BASE )
print(countries_list)

# Declaramos los vectores que poblaremos con datos con los que alimentar el dataFrame
listaPaises = []
salariosMedios = []
preciosCerveza = []
preciosBigMac = []

# recorremos la lista de URL de países 
for country in countries_list:

    web_restaurants = requests.get(
        country['url']+"precio-restaurantes").content
    soup_restaurants = BeautifulSoup(web_restaurants, "html.parser")
    rows = soup_restaurants.find("table").find_all("tr")

    print(country['name'])
    listaPaises.append(country['name'])
    salariosMedios.append(getSalaries(soup_restaurants))
    
    # si solo hay tres columas el precio viene solo en Dólar y Euro
    # por lo que el precio en dólar esta en la columna 1
    if len(rows[0].find_all("td")) == 3:
        i_dolar = 1
    # en caso contraro suponemos que el precio en dólar está en columna 2
    else:
        i_dolar = 2

    if len(rows) > 1:
        beer_price = rows[5].find_all("td")[i_dolar].find(string=True)
        bigmac_price = rows[6].find_all("td")[i_dolar].find(string=True)
    else:
        beer_price = "null"
        bigmac_price = "null"

    preciosCerveza.append(beer_price)
    preciosBigMac.append(bigmac_price)  

    print(country['name'] + "-------------------")
    print("Beer price: " + beer_price)
    time.sleep(1)

fecha_actual = datetime.date.today()
nombre_archivo = f"precios_{fecha_actual}.csv"

to_csv(listaPaises, salariosMedios, preciosCerveza, preciosBigMac, nombre_archivo)