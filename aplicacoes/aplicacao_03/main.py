from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app = Flask(__name__)

class Atracao:
    def __init__(self, nome: str, discografia: str, show: str, cidade: str, data: date ) -> None:
        self.nome = nome
        self.discografia = discografia
        self.show = show
        self.cidade = cidade
        self.data = data

atracoes = []
    

@app.route('/')
def index():
    return render_template('index.html', lista=atracoes)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        discografia = request.form['discografia']
        show = request.form['show']
        cidade = request.form['cidade']
        data = request.form['data']
        nova_atracao = Atracao(nome, discografia, show, cidade, data, )
        atracoes.append(nova_atracao)
        return redirect(url_for('index'))
    
    return render_template('cadastrar_atracao.html')

if __name__ == '__main__':
    app.run(debug=True)

