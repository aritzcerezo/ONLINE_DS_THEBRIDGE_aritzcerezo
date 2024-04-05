'''
En este Script, se definiran las funciones tales que dada una url de 'transfermarkt' que contiene a los jugadores 
de alguno de los equipos de la primera división española de futbol, devuelve un DataFrame con los siguientes datos de
los jugadores: Nombre Completo, Posición, Edad, Nacionalidad (No se considera que hayan obtenido una nueva nacionalidad), y valor de mercado.
'''

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup 
import requests
from fake_useragent import UserAgent    

def get_soup(url):
    '''
    Esta función crea la 'Soup' mediante BeautifulSoup
    '''
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    soup=BeautifulSoup(response.text, 'html.parser')
    return soup

def nombres(soup):
    '''
    Esta función devuelve una lista con los nombres de los jugadores
    '''
    list=[]
    jugadores = soup.find("table", class_="items").find_all("table", class_="inline-table")
    for jug in jugadores:
        link=jug.find("a")
        nombre=link.text.strip()
        list.append(nombre)
    return list


def posiciones(soup):
    '''
    Esta función devuelve una lista con las posiciones de los jugadores
    '''
    list=[]
    jugadores = soup.find("table", class_="items").find_all("td", class_="posrela")
    for jg in jugadores:
        posi=jg.find_all("tr")[-1]
        list.append(posi.text.strip())
    return list

def edades(soup):
    '''
    Esta función devuelve una lista con las edades de los jugadores
    '''
    list=[]
    jugadores = soup.find("table", class_="items").find_all("td",class_="zentriert")
    for i in range(len(jugadores)):
        if i%4==1:
            edad=jugadores[i]   
            list.append(edad.text.strip())
    return list

def nacionalidades(soup):
    '''
    Esta función devuelve una lista con las nacionalidades de los jugadores
    '''
    list=[]
    jugadores = soup.find("table", class_="items").find_all("td",class_="zentriert")
    for i in range(len(jugadores)):
        if i%4==2:
            nac=jugadores[i].find("img")['title']
            list.append(nac)
    return list

def valores(soup):
    '''
    Esta función devuelve una lista con los valores de mercado de los jugadores
    '''
    list=[]
    jugadores = soup.find("table", class_="items").find_all("td", class_="rechts hauptlink")
    for jg in jugadores:
        precio=jg.find("a")
        if precio:
            list.append(precio.text.strip())
        else:
            list.append("Desconocido")
    return list

def crear_df(soup):
    dict = {'Nombre' : nombres(soup),
        'Edad':edades(soup),
        'Posición' : posiciones(soup),
        'Nacionalidad': nacionalidades(soup),
        'Valor_Mercado':valores(soup)
    }
    df=pd.DataFrame(dict)
    return df
    
