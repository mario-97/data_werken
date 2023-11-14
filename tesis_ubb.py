from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import pandas as pd

def es_url_valida(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def obtener_datos_tesis(url_tesis):
    if not es_url_valida(url_tesis):
        print(f'URL no válida: {url_tesis}')
        return None

    response_tesis = requests.get(url_tesis)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response_tesis.status_code == 200:
        soup_tesis = BeautifulSoup(response_tesis.text, 'html.parser')

        # Buscar todas las etiquetas <font> con la clase 'texto-url'
        fonts_texto_url = soup_tesis.find_all('font', class_='texto-url')

        # Si existen fonts_texto_url
        # implica que tiene datos
        # si tiene datos, verificar si hay mas hojas
        # hojas = soup_tesis.find('font', class='text-NAV-index')
        # luego recorrer todos las etiquetas a con href para obtener las url
        # con cada url repetir el ciclo de la linea 40, el for para guardar los datos obtenidos en datos_tesis_lista
        # para ello, debemos crear un nuevo fonts_texto_url para volver a tomar todos los font con clase texto-url, entonces 
        # se deberia tener una funcion que reciba con el for de abajo (linea 40) para repetirlo por cada hoja


        # Lista para almacenar los datos de todos los registros
        datos_tesis_lista = []

        # Iterar sobre todas las instancias de <font> con la clase 'texto-url'
        datos_tesis_lista = iteracion_font_texto_url(fonts_texto_url, datos_tesis_lista)
        hojas = soup_tesis.find('font', class_='texto-NAV-index') # seccion de numeracion de hojas
        if hojas != None:
            for a_tag in hojas.find_all('a', href=True): # tomamos todos las url existentes
                # Obtener el nombre de la etiqueta (texto) y la URL
                num_hoja = a_tag.text # numero de la hoja
                url_sig_hoja = a_tag['href'] # link para visualizar esa hoja 
                # Desglosar la URL para obtener los parámetros necesarios
                url_parts = url_sig_hoja.split('?')
                base_url = url_parts[0]
                parametros = {param.split('=')[0]: param.split('=')[1] for param in url_parts[1].split('&')}

                # Agregar el parámetro 'pag' correspondiente al número de página
                parametros['pag'] = num_hoja 
                # Realizar la solicitud POST con los parámetros
                response_hoja = requests.post('http://werken.ubiobio.cl/' + base_url, data=parametros)
                # Verificar si la solicitud fue exitosa (código de estado 200)
                if response_hoja.status_code == 200:
                    soup_hoja = BeautifulSoup(response_hoja.text, 'html.parser')
                    # Buscar todas las etiquetas <font> con la clase 'texto-url'
                    fonts_texto_url = soup_hoja.find_all('font', class_='texto-url')
                    # Iterar sobre todas las instancias de <font> con la clase 'texto-url'
                    datos_tesis_lista = iteracion_font_texto_url(fonts_texto_url, datos_tesis_lista)

        return datos_tesis_lista
    else:
        print(f'Error al obtener la página. Código de estado: {response_tesis.status_code}')

    return None

def iteracion_font_texto_url(fonts_texto_url, datos_tesis_lista):
    for font_texto_url in fonts_texto_url:
        # Buscar la etiqueta <a> dentro de la etiqueta <font>
        a_tag = font_texto_url.find('a')

        # Verificar si se encontró la etiqueta <a>
        if a_tag:
            # Extraer el texto de la etiqueta <a>
            titulo = a_tag.text

            # Ejemplo de extracción de otros datos
            autor = font_texto_url.find('font', class_='autor').text
            publicacion = font_texto_url.find('font', class_='publicacion').text
            dewey = font_texto_url.find('font', class_='dewey').text

            # Almacenar los datos en un diccionario
            datos_tesis = {
                'titulo': titulo,
                'autor': autor,
                'publicacion': publicacion,
                'dewey': dewey
            }

            # Agregar el diccionario a la lista
            datos_tesis_lista.append(datos_tesis)
    return datos_tesis_lista

def tesis_ubb():
    url = 'http://werken.ubiobio.cl/html/zmemorias.htm'
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Crear un diccionario para almacenar los datos
        datos_dict = {}

        # Encontrar todas las etiquetas <a> y almacenar el valor del atributo href y el texto en el diccionario
        for a_tag in soup.find_all('a', href=True): # si quiero obtener la url numero 3, usar: [2:3]
            # Obtener el nombre de la etiqueta (texto) y la URL
            nombre_etiqueta = a_tag.text
            url_tesis = a_tag['href']

            # Verificar si la URL es válida antes de procesarla
            if es_url_valida(url_tesis):
                # Procesar la URL para obtener los datos de la tesis
                datos_tesis = obtener_datos_tesis(url_tesis)

                # Almacenar en el diccionario principal
                if datos_tesis:
                    datos_dict[nombre_etiqueta] = datos_tesis
            else:
                print(f'URL no válida: {url_tesis}')

        # Devolver el diccionario principal
        return datos_dict
    else:
        print(f'Error al obtener la página. Código de estado: {response.status_code}')
        return None
 