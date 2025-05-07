from flask import Flask , url_for, render_template, request

import sqlite3

app = Flask(__name__)

db = None

def dict_factory(cursor, row):
  """Arma un diccionario con los valores de la fila."""
  fields = [column[0] for column in cursor.description]
  return {key: value for key, value in zip(fields, row)}

def abrirConexion():
   global db
   db = sqlite3.connect("instance/datos.sqlite")
   db.row_factory = dict_factory

def cerrarConexion():
   global db
   db.close()
   db = None

@app.route("/test-db")
def testDB():
   abrirConexion()
   cursor = db.cursor()
   cursor.execute("SELECT COUNT(*) AS cant FROM usuarios; ")
   res = cursor.fetchone()
   registros = res["cant"]
   cerrarConexion()
   return f"Hay {registros} registros en la tabla usuarios"

@app.route("/agregar")
def agregar_usuario():
    abrirConexion()
    cursor = db.cursor()
    #usuario = request.args.get("usuario")  Para agregar desde la URL
    #email = request.args.get("email")      http://127.0.0.1:5000/agregar?usuario=Pedro&email=pedro@mail.com
    usuario ="juan" 
    email ="juan@gmail.com"
    cursor.execute("INSERT INTO usuarios(usuario,email) VALUES (?,?)",(usuario,email))
    db.commit()  # muy importante para guardar los cambios
    cerrarConexion()
    return f"Usuario {usuario} agregado con email {email}"

@app.route("/borrar/<int:id>")
def borrar_usuario():
    abrirConexion()
    cursor = db.cursor()
    #id = request.argst.get("id")    para agregar desde la url
    #http://127.0.0.1:5000/borrar?id=2
    cursor.execute("DELETE FROM usuarios WHERE id =?",(id,))
    db.commit()
    cerrarConexion()
    return f"se Borro el usuario con ID {id}"

@app.route("/MostrarPorID/<int:id>")
def nombre_email_usurio(id):
    abrirConexion()
    cursor = db.cursor()
    #http://127.0.0.1:5000/2
    cursor.execute("SELECT usuario ,email FROM usuarios WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    cerrarConexion()
    return f"mostrar{resultado["usuario"]} y email {resultado["email"]} "

@app.route("/mostrar-datos-plantilla/<int:id>")
def datos_plantilla(id):
    abrirConexion()
    cursor = db.cursor()
    cursor.execute("SELECT id,usuario ,email,telefono,direccion FROM usuarios WHERE id = ?", (id,))
    res = cursor.fetchone()
    cerrarConexion()
    usuario = None
    email = None 
    telefono = None
    direccion = None
    if res != None:
       usuario = res['usuario']
       email = res['email']
       telefono = res['telefono']
       direccion = res['direccion']
    return render_template("datos2.html", id=id, usuario=usuario, email=email , telefono=telefono, direccion=direccion )
   


@app.route("/")
def principal():
    return """
        <a href="{url_for('saludar')}">Saludar</a><br>
        <a href="{url_for('despedir')}">Despedir</a><br>
        <a href="{url_for('dado', caras=6)}">Tirar dado de 6</a><br>
        <a href="{url_for('dado', caras=20)}">Tirar dado de 20</a><br>
    """

@app.route("/hola")
def saludar():
    return "<p>Hello, World!</p>"

@app.route("/chau")
def despedir():
    return "<p>Bye, World!</p>"

@app.route("/dado/<int:caras>")
def dado(caras):
    from random import randint
    numero = randint(1,caras)
    return f"<h2>Dado de {caras} caras, salio {numero}!</h2>"


