#datos_estudios
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
#from redis import Redis
import redis

app = Flask(__name__)
client = MongoClient('mongodb://db:27017/')
#db2 = client.curriculumDBEstudio
db = client.curriculumDB
cache = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route('/datos_estudios')
def get_datos_estudios():
    #// buscar dni     #cache.setex("datos_generales", 3600, datos_generales)
#
    data = db.datos_estudios.find_one()
    if not data:
        #return "No hay datos disponibles", 200

        return redirect(url_for('list_datos_estudios'))
    #return render_template('pant_datos.html', data=data,datos_generales=datos_generales)
    return render_template('pant_datos.html', data=data)

@app.route('/add_datos_estudios', methods=['GET', 'POST'])
def add_datos_estudios():
    if request.method == 'POST':
        # Recopilar datos del formulario
        dni = request.form.get('dni')
        estudio = request.form.get('estudio')
        entidad = request.form.get('entidad')
        fecha_termino = request.form.get('fecha_termino')

        # Insertar en la base de datos
        db.datos_estudios.insert_one({
            "dni": dni,
            "estudio": estudio,
            "entidad": entidad,
            "fecha_termino": fecha_termino
        })
        # ojo ultimo
        #data = db.datos_estudios.find_one({"dni": dni})   
        return redirect(url_for('get_datos_estudios'))
    return render_template('add_datos.html')
    
@app.route('/list_datos_estudios')
def list_datos_estudios():
    data = list(db.datos_estudios.find())
    db_ge = db[ "datos_generales"]
    data2 = db_ge.find({"dni": 242424})
    print(data2)
    
    if not data:
        #return "No hay datos crud list ", 404
    #return render_template('list_datos.html', data=data)
        return render_template('list_datos.html', data=data)
    return render_template('list_datos.html', data=data)

@app.route('/edit_datos_estudios/<dni>', methods=['GET', 'POST'])
def edit_datos_estudios(dni):
    print(f"Editing DNI: {dni}")
    data = db.datos_estudios.find_one({"dni": dni})
    if not data:
        return "DNI no encontrado", 404

    if request.method == 'POST':
        # Recopilar datos actualizados del formulario
        estudio = request.form.get('estudio')
        entidad = request.form.get('entidad')
        fecha_termino = request.form.get('fecha_termino')

        # Actualizar en la base de datos
        db.datos_estudios.update_one({"dni": dni}, {
            "$set": {
                "estudio": estudio,
                "entidad": entidad,
                "fecha_termino": fecha_termino
            }
        })

        return redirect(url_for('get_datos_estudios'))
    return render_template('edit_datos.html', data=data)

@app.route('/update_datos_estudios/<dni>', methods=['POST'])
def update_datos_estudios(dni):
    if request.method == 'POST':
        # Recopilar datos actualizados del formulario
        estudio = request.form.get('estudio')
        entidad = request.form.get('entidad')
        fecha_termino = request.form.get('fecha_termino')

        # Actualizar en la base de datos
        db.datos_estudios.update_one({"dni": dni}, {
            "$set": {
                "estudio": estudio,
                "entidad": entidad,
                "fecha_termino": fecha_termino
            }
        })

        return redirect(url_for('list_datos_estudios'))

@app.route('/delete_datos_estudios/<dni>', methods=['POST'])
def delete_datos_estudios(dni):
    db.datos_estudios.delete_one({"dni": dni})
    return redirect(url_for('list_datos_estudios'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
