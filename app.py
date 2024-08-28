from flask import Flask, render_template, request, redirect, session


app = Flask(__name__)


app.secret_key = 'aprendendoflasksupermodulo'


class Time:
    def __init__(self, nome: str, estado: str, apelido: str) -> None:
        self.nome = nome
        self.estado = estado
        self.apelido = apelido


class Banda:
    def __init__(self, nome_banda: str, musica: str, show: str,
                 data: str,
                 cidade: str) -> None:
        self.nome_banda = nome_banda
        self.musica = musica
        self.show = show
        self.data = data
        self.cidade = cidade


time1 = Time('Flamengo', 'Rio de Janeiro', 'Mengão')
time2 = Time('Palmeiras', 'São Paulo', 'Sem mundial')
time3 = Time('Bahia', 'Bahia', 'Bahea')

lista_times = [time1, time2, time3]


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


@app.route('/cadastrar-show')
def cadastrar_show():
    return render_template('cadastrar_show.html')


lista_bandas = []


@app.route('/add', methods=['POST',])
def add():
    nome_banda = request.form['nome_banda']
    musica = request.form['musica']
    show = request.form['show']
    data = request.form['data']
    cidade = request.form['cidade']

    novaBanda = Banda(
        nome_banda=nome_banda,
        musica=musica,
        show=show,
        data=data, cidade=cidade)

    lista_bandas.append(novaBanda)

    print(len(lista_bandas))

    return render_template('home_bandas.html', lista=lista_bandas)


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
