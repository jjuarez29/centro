#from flask import Flask
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from redis import Redis


# Inicializar la aplicación y la conexión a la base de datos
app = Flask(__name__)
#client = MongoClient('mongodb://mongodb:27017/')  debe se db:27017  no se usa principal
#db = client.curriculumDB

# Importar el módulo que contiene las rutas para datos_generales.
# Asegurándonos de que las rutas definidas en ese módulo se registren en la app.
from microfrontends.datos_generales import main
from microfrontends.datos_estudios  import main

@app.route('/')
def inicio():
    return render_template('/inicio.html')

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5001)
    app.run(host='0.0.0.0', port=5000)

