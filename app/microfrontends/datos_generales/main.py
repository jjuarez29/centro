#datos_generales
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from redis import Redis

app = Flask(__name__)
client = MongoClient('mongodb://db:27017/')
db = client.curriculumDB
redis_client = Redis(host='redis', port=6379, db=0, decode_responses=True)  # Asegúrate de que 'redis' sea el nombre del servicio en tu docker-compose


@app.route('/datos_generales')
def get_datos_generales():
    data = db.datos_generales.find_one()
    if not data:
        return "No hay datos disponibles", 200
    #return render_template('datos_generales.html', data=data)
    return render_template('list_datos_crud.html',data=data)

@app.route('/add_datos_generales', methods=['GET', 'POST'])
def add_datos_generales():
    if request.method == 'POST':
        # Recopilar datos del formulario
        dni = request.form.get('dni')
        apellidos = request.form.get('apellidos')
        nombres = request.form.get('nombres')
        fecha_nacimiento = request.form.get('fecha_nacimiento')

        # Insertar en la base de datos
        result=db.datos_generales.insert_one({
            "dni": dni,
            "apellidos": apellidos,
            "nombres": nombres,
            "fecha_nacimiento": fecha_nacimiento
        })

        # Insertar en Redis
        # Utilizamos el ID generado por MongoDB como clave en Redis
        redis_key = f"datos_generales:{result.inserted_id}"
        redis_client.hset(redis_key, mapping={
            "dni": dni,
            "apellidos": apellidos,
            "nombres": nombres,
            "fecha_nacimiento": fecha_nacimiento
        })


        return redirect(url_for('get_datos_generales'))
    return render_template('add_datos_generales.html')
    #return render_template('list_datos_crud.html')


@app.route('/list_datos_generales')
def list_datos_generales():
    data = list(db.datos_generales.find())
    return render_template('list_datos_generales.html', data=data)

@app.route('/list_datos_crud')
def list_datos_crud():
    data = list(db.datos_generales.find())
    print("llego ok")
    if not data:
        #return "No hay datos crud list ", 404
        #return redirect(url_for('add_datos_generales'))
        return render_template('list_datos_crud.html', data=data)
    return render_template('list_datos_crud.html', data=data)


@app.route('/edit_datos_generales/<dni>', methods=['GET', 'POST'])
def edit_datos_generales(dni):
    print(f"Editing DNI: {dni}")  # Agregamos una impresión para depuración
    data = db.datos_generales.find_one({"dni": dni})
    if not data:
        return "DNI no encontrado", 404

    if request.method == 'POST':
        # Recopilar datos actualizados del formulario
        apellidos = request.form.get('apellidos')
        nombres = request.form.get('nombres')
        fecha_nacimiento = request.form.get('fecha_nacimiento')

        # Actualizar en la base de datos
        db.datos_generales.update_one({"dni": dni}, {
            "$set": {
                "apellidos": apellidos,
                "nombres": nombres,
                "fecha_nacimiento": fecha_nacimiento
            }
        })

        return redirect(url_for('get_datos_generales'))
    return render_template('edit_datos_generales.html', data=data)
    #return render_template('list_datos_crud.html')

@app.route('/update_datos_generales/<dni>', methods=['POST'])
def update_datos_generales(dni):
    if request.method == 'POST':
        # Recopilar datos actualizados del formulario
        apellidos = request.form.get('apellidos')
        nombres = request.form.get('nombres')
        fecha_nacimiento = request.form.get('fecha_nacimiento')

        # Actualizar en la base de datos
        db.datos_generales.update_one({"dni": dni}, {
            "$set": {
                "apellidos": apellidos,
                "nombres": nombres,
                "fecha_nacimiento": fecha_nacimiento
            }
        })

        return redirect(url_for('list_datos_crud'))

@app.route('/delete_datos_generales/<dni>', methods=['POST'])
def delete_datos_generales(dni):
    db.datos_generales.delete_one({"dni": dni})
    return redirect(url_for('list_datos_crud'))

#@app.route('/')
#def index():
    # Esta es la vista que renderiza index.html cuando se accede a la URL base.
 #   return render_template('index.html')

@app.route('/rindex')
def rindex():
    #return urender_template('inicio.html')

    return redirect('http://localhost:5000/')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
