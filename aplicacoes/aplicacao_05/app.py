from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

app.secret_key = 'aprendendoflasksupermodulo'

class Time:
    def __init__(self, nome: str, estado: str, apelido: str) -> None:
        self.nome = nome
        self.estado = estado
        self.apelido = apelido

lista_times = []

@app.route('/')
def index():
    return render_template('index.html', lista=lista_times)

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar_time.html')

@app.route('/adicionar', methods=['POST',])
def adicionar_time():
    nome = request.form['nome']
    estado = request.form['estado']
    apelido = request.form['apelido']

    novoTime = Time(nome=nome, estado=estado, apelido=apelido)

    lista_times.append(novoTime)

    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['senha'] == 'Teste1234':
        session['usuario_logado'] = request.form['login']
        return redirect('/')
    return redirect('/login')

@app.route('/sair')
def sair():
    session['usuario_logado'] = None
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)