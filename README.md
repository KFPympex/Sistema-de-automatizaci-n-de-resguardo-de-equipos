# Sistema de automatización de resguardo de equipos.

# NOTA
**Este proyecto se debe de descargar y correr de manera local para que funcione de manera correcta**

## Pasos a seguir

## 1. Crea un Virtual Enviroment **en caso de no querer instalar las dependencias de manera local**

````shell
python3 -m venv .venv
````

## 2. Avtivar el Virtual Enviroment

````shell
.venv/Scripts/activate
````

## 3. Desactivar el Virtual Enviroment

````shell
deactivate
````

## 4. Actualizar PIP

````shell
pip install --upgrade pip
````

## 5. Instalar la conexion de Python con MySQL
````shell
pip install mysql-connector-python
````

## 6. Instalar Web.py
````shell
pip install web.py
````

## 7. Instalar bcrypt para hashear las contraseñas
````shell
pip install bcrypt
````

## 8. Instalar PyPDF2 y reportlab para sobreescribir en el PDF de Resguardos original.
````shell
pip install reportlab PyPDF2 
````

## 9. Crear el archivo requirements

````shell
pip freeze > requirements.txt
````

## 10. Crear el archivo runtime

````shell
python -V > runtime.txt
````

## 11. Iniciar app

````shell
python app.py 127.0.0.1
````

