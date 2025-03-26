from flask import Flask

app = Flask(__name__)

@app.route("/")
def principal():
    return """
        <a href='/hola'>saludar</a>
        <a href='/chau'>despedir</a>
    """

@app.route("/hola")
def saludar():
    return "<p>Hello, World!</p>"

@app.route("/chau")
def despedir():
    return "<p>Bye, World!</p>"

