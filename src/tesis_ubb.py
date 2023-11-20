from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs, urlunparse

def transformar_url(url, info_url):
    # Parsear las URL
    parsed_url = urlparse(url)
    parsed_info_url = urlparse(info_url)

    # Extraer la ruta y parámetros de la segunda URL
    path_info_url = parsed_info_url.path
    query_info_url = parsed_info_url.query

    # Construir la nueva URL
    nueva_url = urlunparse((parsed_url.scheme, parsed_url.netloc, path_info_url, parsed_info_url.params, query_info_url, parsed_info_url.fragment))

    return nueva_url


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

        # Lista para almacenar los datos de todos los registros
        datos_tesis_lista = [] 
        # Iterar sobre todas las instancias de <font> con la clase 'texto-url'
        datos_tesis_lista = iteracion_font_texto_url(fonts_texto_url, datos_tesis_lista, url_tesis)
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
                    datos_tesis_lista = iteracion_font_texto_url(fonts_texto_url, datos_tesis_lista, url_tesis)

        return datos_tesis_lista
    else:
        print(f'Error al obtener la página. Código de estado: {response_tesis.status_code}')

    return None

def iteracion_font_texto_url(fonts_texto_url, datos_tesis_lista, url):
    for font_texto_url in fonts_texto_url:
        # Buscar la etiqueta <a> dentro de la etiqueta <font>
        a_tag = font_texto_url.find('a')

        # Verificar si se encontró la etiqueta <a>
        if a_tag:
            # Extraer el texto de la etiqueta <a>
            titulo = a_tag.text
            # link para visualizar ese item
            info_url = "php/" + a_tag['href'] 
            # Ejemplo de extracción de otros datos
            autor = font_texto_url.find('font', class_='autor').text
            publicacion = font_texto_url.find('font', class_='publicacion').text
            dewey = font_texto_url.find('font', class_='dewey').text 
            # Inicializar listas vacías para almacenar los resultados
            nueva_datos_adicionales = {}  
            # url de acceso directo a mas informacion del item seleccionado
            """ acceso_info_url = transformar_url(url, info_url).replace("existencias", "resumen_total")  
            
            try:
                # Realizar la solicitud GET con los parámetros
                response_info_url = requests.get(acceso_info_url, timeout=10)
                # Asegurarse de que la respuesta sea exitosa
                response_info_url.raise_for_status()
                # Verificar si la solicitud fue exitosa (código de estado 200)
                if response_info_url.status_code == 200:
                    soup_info_url = BeautifulSoup(response_info_url.text, 'html.parser')

                    # Encuentra la tabla o elemento que contiene la información deseada
                    # Aquí estoy suponiendo que hay una tabla, ajusta según la estructura real de tu página
                    tabla_info = soup_info_url.find_all('table') 
                    tabla_info = tabla_info[1] # en el html existen dos tablas, hay que tomar la segunda

                    # Inicializar listas para almacenar los datos adicionales
                    datos_adicionales_izquierda = []
                    datos_adicionales_derecha = []

                    # Verificar si se encontró la tabla
                    if tabla_info:
                        # Encontrar todas las filas de la tabla
                        filas_info = tabla_info.find_all('tr')

                        # Iterar sobre las filas
                        for fila_info in filas_info:
                            # Encontrar todas las celdas de la fila
                            celdas_info = fila_info.find_all('td')

                            # Verificar si hay al menos dos celdas (izquierda y derecha)
                            if len(celdas_info) == 2:
                                # Agregar datos a las listas correspondientes
                                datos_adicionales_izquierda.append(celdas_info[0].get_text(strip=True))
                                datos_adicionales_derecha.append(celdas_info[1].get_text(strip=True))
                    
                    temp = ""
                    # Iterar sobre las dos listas
                    for i in range(len(datos_adicionales_izquierda)): 
                        # Si el elemento actual de datos_adicionales_izquierda no está en blanco, agregarlo a la lista
                        if datos_adicionales_izquierda[i] != "":
                            nueva_datos_adicionales[datos_adicionales_izquierda[i]] = datos_adicionales_derecha[i]
                            temp = datos_adicionales_izquierda[i]
                        else:
                            # Si el elemento actual de datos_adicionales_izquierda está en blanco, agregar el elemento de datos_adicionales_derecha al elemento anterior
                            nueva_datos_adicionales[temp] = nueva_datos_adicionales[temp] + " | " + datos_adicionales_derecha[i]

            except requests.exceptions.RequestException as e:
                print(f"Error en la solicitud para {acceso_info_url}: {e}")
                continue  # Saltar a la siguiente iteración en caso de error 
            """
            # Almacenar los datos en un diccionario
            datos_tesis = {
                'titulo': titulo,
                'autor': autor,
                'publicacion': publicacion,
                'dewey': dewey,
                'datos_de_publicacion': nueva_datos_adicionales.get('Datos de Publicación :', None),
                'otros_autores': nueva_datos_adicionales.get('Otro(s) Autor(es) :', None)
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

        contador = 1
        # Encontrar todas las etiquetas <a> y almacenar el valor del atributo href y el texto en el diccionario
        for a_tag in soup.find_all('a', href=True): # si quiero obtener la url numero 3, usar: [2:3]
            # Obtener el nombre de la etiqueta (texto) y la URL
            nombre_etiqueta = a_tag.text
            print("Indice: ", contador)
            print("Materia: ", nombre_etiqueta)
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

            contador = contador + 1

        datos_tesis_dict = datos_dict
        # Crear un DataFrame de pandas
        df = pd.DataFrame([(materia, tesis["titulo"], tesis["autor"], tesis["publicacion"], tesis["dewey"], tesis["datos_de_publicacion"], tesis["otros_autores"]) 
                    for materia, tesis_lista in datos_tesis_dict.items() 
                    for tesis in tesis_lista],
                    columns=["Materia", "Título", "Autor", "Publicación", "Dewey", "datos_de_publicacion", "otros_autores"])
        print(df)
        
        # Devolver el diccionario principal
        return df
    else:
        print(f'Error al obtener la página. Código de estado: {response.status_code}')
        return None
    

""" # Ejemplo de uso
datos_para_power_bi = tesis_ubb()
print(datos_para_power_bi) """
 