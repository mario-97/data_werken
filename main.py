from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Optional
from tesis_ubb import tesis_ubb
from json_to_excel import json_to_excel

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
    return tesis_ubb()


@app.get("/data_json")
def data_export():
    excel_file = json_to_excel()
    response = Response(content=excel_file)
    response.headers["Content-Disposition"] = "attachment; filename=tesis_data.xlsx"
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return response  