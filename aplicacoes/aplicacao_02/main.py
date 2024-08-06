from flask import Flask, render_template

app = Flask(__name__)

@app.route('/<nome>')
def home(nome):
    return f'Seja bem-vindo a minha aplicação {nome}'

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

if __name__ == '__main__':
    app.run()