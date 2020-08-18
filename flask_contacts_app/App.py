'''
Importamos el modulo Flask de flask, render template: es para renderizar para pagina,
Redirect: redirecciona la página.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
'''
Importamos el modulo mysql para realizar nuestra conexión a la base de datos.
'''
from flask_mysqldb import MySQL

'''
creamos la variable app(el cual nos servirá para ejecutar nuestro servidor) para hacer referencia a la clase Flask(),
el cual va a recibir un parámetro __name__
'''
app = Flask(__name__)
# Hacemos una llamada al archivo mysql_connect, para utilizar los datos de configuración de la bd.
app.config.from_pyfile('mysql_connect.py')
# establecemos una variable para hacer uso de las funcionales(modulos) de Mysql.
db = MySQL(app)
'''
Con el decorador @app hacemos una llamada al modulo route, para establecer las rutas de navegación con las que contará nuestra app.
En éste caso establecemos la ruta
'''
@app.route('/')
def Index():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

# Agregamos la ruta add?contact, el cual se encargará de agregar o registrar datos en la base de datos.
# Establecemos el metodo en el cual se enviarán los datos, para éste caso usaremos el metodo POST.
@app.route('/add_contact', methods=['POST'])
def add_contact():
    #Verificamos que los datos recividos sean enviados por el metodo POST.
    if request.method == 'POST':
       fullname = request.form['fullname']
       phone = request.form['phone']
       email = request.form['email']
       #Establecemos la conexión con la base de datos.
       cur = db.connection.cursor()
       #Ejecutamos el comando para insertar los datos en la base de datos.
       cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
       # Confirmamos y cerramos la conexión a la base de datos.
       db.connection.commit()
       flash('Contacto agregado satifactoriamente.')
       return redirect(url_for('Index'))

@app.route('/edit/<string:id>')
def get_contact(id):
    #Establecemos la conexión con la base de datos.
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM contacts where id = {0}".format(id))
    data = cur.fetchall()
    return render_template("edit-contact.html", contact = data[0])

#Agregamos una ruta edit, el cual se encargará de editar los datos de la base de datos.
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = db.connection.cursor()
        cur.execute("UPDATE contacts set fullname = %s, phone = %s, email = %s WHERE id = %s", (fullname, phone, email, id))
        cur.connection.commit()
        flash('Contacto actualizado satifactoriamente.')
        return redirect(url_for('Index'))


#Agregamos una ruta delete, que se encargará de eliminar los datos de la base de datos.
@app.route('/delete/<string:id>')
def delete_contact(id):
    print(id)
    if id:
        cur = db.connection.cursor()
        cur.execute("DELETE FROM contacts where id = {0}".format(id))
        db.connection.commit()
        flash('Contacto ha sido eliminado satifactoriamente.')
        return redirect(url_for('Index'))
'''
Verificamos que la función principal es la que se está ejecutando.
'''
if __name__ == 'main':
    '''
    Establecemos la configuración de nuestro servidor, definiendo el puerto y el modo en que se va a comportar.
    debug=true nos ahorra reiniciar el server despues de cualquier modificación. 
    '''
    app.run(port=5000, debug=True)
