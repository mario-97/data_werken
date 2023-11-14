import json
import pandas as pd
from io import BytesIO
def json_to_excel():  
    # Cargar datos desde el archivo JSON con codificación utf-8
    with open('datos.json', 'r', encoding='utf-8') as f:
        datos_tesis_dict = json.load(f)

    # Crear un DataFrame de pandas
    df = pd.DataFrame([(materia, tesis["titulo"], tesis["autor"], tesis["publicacion"], tesis["dewey"]) 
                    for materia, tesis_lista in datos_tesis_dict.items() 
                    for tesis in tesis_lista],
                    columns=["Materia", "Título", "Autor", "Publicación", "Dewey"])

    # Guardar el DataFrame en un archivo Excel y obtener el contenido binario
    excel_content = BytesIO()
    df.to_excel(excel_content, index=False, engine='xlsxwriter')
    excel_content.seek(0)  # Posicionar el cursor al principio para que se pueda leer

    # Convertir el contenido binario a bytes
    excel_bytes = excel_content.read()

    return excel_bytes