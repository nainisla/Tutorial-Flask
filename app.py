from flask import Flask , url_for
import sqlite3

app = Flask(__name__)

db=None

def AbrirConexion():
    global db
    db = sqlite3.connect('instance/datos.sqlite')
    db.row_factory= sqlite3.Row
    return db

def CerrarConexion():
    global db
    if db is not None:
        db.close()
        db=None

@app.route("/usuarios/")
def ObtenerGente():
    global db
    conexion = AbrirConexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM usuarios')
    resultado = cursor.fetchall()
    CerrarConexion()
    fila = [dict(row) for row in resultado]
    return str(fila)

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


