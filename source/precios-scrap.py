import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import datetime
import os


def get_precios_transporte(country, i_col):
    '''
      Esta Función nos devuelve el precio de un billete de transporte
      el precio de inicio de taxi y el precio de 1Km de Taxi para un país
      dado y un índice de columna dado
      Ej invocación:
      precioBillete, inicioTaxi, taxi1Km = get_precios_transporte(
        country, i_dolar)
    '''
    web_services = requests.get(
        country['url']+"precio-transporte-servicios").content
    soup_services = BeautifulSoup(web_services, "html.parser")
    rows = soup_services.find("table").find_all("tr")

    # i_taxi1h = getIndexOf('Taxi 1km (tarifa normal)', rows)
    # i_inicio_taxi = getIndexOf('Inicio taxi (tarifa normal)', rows)

    precioBillete = getPriceOf(
        'Un billete de ida en transporte público', rows, i_col)
    inicioTaxi = getPriceOf(
        'Inicio taxi (tarifa normal)', rows, i_col)
    taxi1Km = getPriceOf(
        'Taxi 1km (tarifa normal)', rows, i_col)

    print("Public transport ticket price: " + precioBillete)
    return precioBillete, inicioTaxi, taxi1Km


def to_csv(listaPaises, salariosMedios, preciosCola, preciosCerveza, preciosBigMac, preciosBillete,
           precios1KmTaxi, preciosInicioTaxi, preciosCapuccino, preciosMenuDelDia, nombre_archivo):
    '''
      Esta función crea un dataframe a partir de las listas de precios pasadas como
      parámetro y lo exporta a un fichero CSV pasado por parámetro
    '''
    # Crear un diccionario con los datos
    data = {'Pais': listaPaises,
            'Salario Medio': salariosMedios,
            'Refresco': preciosCola,
            'Capuccino': preciosCapuccino,
            'Cerveza': preciosCerveza,
            'Menú Big Mac': preciosBigMac,
            'Menú del día': preciosMenuDelDia,
            'Billete transporte': preciosBillete,
            'Inicio Taxi': preciosInicioTaxi,
            'Taxi 1Km': precios1KmTaxi
            }

    # Crear un DataFrame a partir del diccionario
    dataFrame = pd.DataFrame(data)

    # Escribir la información del DataFrame en un archivo csv
    dataFrame.to_csv(nombre_archivo, index=False)

# buscamos en la página de cada continente los links
# base de todos los países que guardaremos en countries_list


def getCountriesList(continentes, URL_BASE):
    '''
      Esta función devuelve el listado de países completo
      de una lista de continentes dada y la URL_BASE del sitio web.
      Devuelve una lista de países.
    '''
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


def getPriceOf(priceDefinition, rows, i_col):
    '''
      Devuelve el valor del precio dado por:
      priceDefinition: Definición del precio tal cual sale en preciosmundi
      rows: lista de elementos <tr> de la tabla
      i_col: índice de la columna para el precio
    '''
    value = "null"
    for row in rows:
        tds = row.find_all("td")
        if tds:
            if tds[0].find(string=True) == priceDefinition:
                value = tds[i_col].find(string=True)
    return value


def getSalaries(soup_restaurants):
    '''
      Esta función extrae de un objeto soup de BS4 (con estructura
      de página de restaurantes de nuestro sitio web) el salario
      medio para el país de esa página, devolviéndolo finalmente.
    '''
    aside_lis = soup_restaurants.select(".container aside li")
    # print(aside_lis[1])
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
continentes = ['europa', 'america', 'asia', 'africa', 'oceania']

countries_list = getCountriesList(continentes, URL_BASE)
print(countries_list)

# Declaramos los vectores que poblaremos con datos con los que alimentar el dataFrame
listaPaises = []
salariosMedios = []
preciosCerveza = []
preciosBigMac = []
preciosBillete = []
preciosCola = []
preciosInicioTaxi = []
precios1KmTaxi = []
preciosMenuDelDia = []
preciosCapuccino = []


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
    # por lo que el precio en euros esta en la columna 2
    if len(rows[0].find_all("th")) == 3:
        i_euro = 2
    # en caso contrario suponemos que hay una columna más de precios
    # para el precio en moneda loca, por lo que
    # el precio en euros está en columna 3
    else:
        i_euro = 3

    cola_price = getPriceOf(
        'Coca-Cola / Pepsi (botella de 33cl) ', rows, i_euro)
    beer_price = getPriceOf('Cerveza nacional (0,5 litros) ', rows, i_euro)
    bigmac_price = getPriceOf(
        'Menú de McDonalds, Burger King o similar', rows, i_euro)
    capuccino_price = getPriceOf('Café Cappuccino ', rows, i_euro)
    menudia_price = getPriceOf(
        'Comida en un restaurante barato (menú del día)', rows, i_euro)

    preciosCola.append(cola_price)
    preciosCerveza.append(beer_price)
    preciosBigMac.append(bigmac_price)
    preciosCapuccino.append(capuccino_price)
    preciosMenuDelDia.append(menudia_price)

    print(country['name'] + "-------------------")
    print("Beer price: " + beer_price)
    time.sleep(1)

    # Obtenemos y almacenamos el precio de un billete de ida en transporte público
    # el precio inicial de un taxi y el precio por Km de un taxi
    precioBillete, inicioTaxi, taxi1Km = get_precios_transporte(
        country, i_euro)
    preciosBillete.append(precioBillete)
    precios1KmTaxi.append(taxi1Km)
    preciosInicioTaxi.append(inicioTaxi)
    time.sleep(1)

fecha_actual = datetime.date.today()

# Comprobamos que existe el directorio dataset en la carpeta de destino y si no lo creamos
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

nombre_archivo = os.path.join(dataset_path, f"precios_{fecha_actual}.csv")

to_csv(listaPaises, salariosMedios, preciosCola, preciosCerveza,
       preciosBigMac, preciosBillete, precios1KmTaxi, preciosInicioTaxi,
       preciosCapuccino, preciosMenuDelDia, nombre_archivo)
