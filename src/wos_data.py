import requests
from bs4 import BeautifulSoup

def wos_data(url, usuario, contrasena):
    # Crear una sesión para mantener la conexión
    sesion = requests.Session()

    try:
        # Enviar una solicitud GET para obtener el formulario de inicio de sesión
        response = sesion.get(url)

        # Analizar el contenido HTML de la página para extraer datos del formulario de inicio de sesión
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar el formulario de inicio de sesión y extraer los campos necesarios
        form = soup.find('form')
        action = form['action']
        inputs = form.find_all('input', {'type': ['text', 'password', 'hidden']})

        # Crear un diccionario con los datos del formulario de inicio de sesión
        datos_inicio_sesion = {input['name']: input.get('value', '') for input in inputs}
        datos_inicio_sesion['username'] = usuario
        datos_inicio_sesion['password'] = contrasena

        # Enviar una solicitud POST con las credenciales de inicio de sesión
        sesion.post(action, data=datos_inicio_sesion)

        # Ahora puedes realizar solicitudes adicionales con la sesión autenticada
        response = sesion.get(url)

        # Retornar el HTML de la página autenticada
        return response.text

    finally:
        # Cerrar la sesión cuando hayas terminado, incluso si ocurre una excepción
        sesion.close()
