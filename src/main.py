from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Optional
from tesis_ubb import tesis_ubb
from json_to_excel import json_to_excel
from dataciencia import data_sciencia_download
from wos_data import wos_data
import time

app = FastAPI()

class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: Optional[str]

@app.get("/") # @  con es simbolo registramos la funcion
def index():
    return {"message": "Hola wapos"}

@app.get("/webscraping")
def data_tesisubb():
    tiempo_inicial = time.time()
    response = tesis_ubb()
    tiempo_final = time.time()
    print("Minutos =", (tiempo_final - tiempo_inicial)/60)	
    return response


@app.get("/data_json")
def data_export():
    tiempo_inicial = time.time()
    excel_file = json_to_excel()
    response = Response(content=excel_file)
    response.headers["Content-Disposition"] = "attachment; filename=tesis_data.xlsx"
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    tiempo_final = time.time()
    print("Minutos =", (tiempo_final - tiempo_inicial)/60)	
    return response  

@app.get("/download_anid")
def data_export_anid():      
    tiempo_inicial = time.time()
    # URL del archivo CSV
    url_scielo = "https://dataciencia.anid.cl/articles/breakdown/csv?indexation%5B%5D=SciELO&institution_id%5B%5D=3&limit=50&page=1" # SciELO
    url_wos =    "https://dataciencia.anid.cl/articles/breakdown/csv?indexation%5B%5D=WoS&institution_id%5B%5D=3&limit=50&page=1" # Wos
    url_scopus = "https://dataciencia.anid.cl/articles/breakdown/csv?indexation%5B%5D=Scopus&institution_id%5B%5D=3&limit=50&page=1" # Scopus
    response = data_sciencia_download(url_scielo)
    tiempo_final = time.time()
    print("Minutos =", (tiempo_final - tiempo_inicial)/60)	
    return response

@app.get("/download_wos")
def wos_datos():
    # Ejemplo de uso
    url_a_scrapear = "https://www.webofscience.com/wos/author/results/1/relevance/2"
    usuario = "mulloao@ubiobio.cl"
    contrasena = "12Mario3_"

    html_autenticado = wos_data(url_a_scrapear, usuario, contrasena)

    # Ahora puedes trabajar con el HTML obtenido
    return html_autenticado

 