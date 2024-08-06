from flask import Flask

app = Flask(__name__)

@app.route('/')
def ola():
    return 'Olá, Mundo!'

@app.route('/minha-segunda-rota')
def ola_dois():
    return 'Olá, Mundo de novo!'