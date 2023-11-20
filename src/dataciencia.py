import requests 
import pandas as pd
from io import StringIO 

def data_sciencia_download(url):
    try:
        # Realiza la solicitud GET al URL
        response = requests.get(url)

        # Verifica si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Obtén el contenido del CSV
            contenido_csv = response.text

            # Convierte el contenido CSV en un DataFrame de pandas
            dataframe = pd.read_csv(StringIO(contenido_csv), delimiter='\t')

            # Imprime el DataFrame
            print(dataframe)
            
            # Retorna el csv
            return contenido_csv

        else:
            print(f"Error al cargar el archivo. Código de estado: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")
