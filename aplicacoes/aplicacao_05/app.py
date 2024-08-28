from flask import Flask, render_template, request, redirect, session, url_for, flash
from db.connection import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

class Time:
    def __init__(self, nome: str, estado: str, apelido: str) -> None:
        self.nome = nome
        self.estado = estado
        self.apelido = apelido

lista_times = []

@app.route('/')
def index():
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado para ver esta página.', 'warning')
        return redirect(url_for('login'))
    
    conexao = get_db_connection()
    cursor = conexao.cursor()

    try:
        user_id = session['usuario_logado']
        cursor.execute("SELECT * FROM times WHERE usuario_id_time = %s", (user_id,))
        lista_times = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Erro ao acessar o banco de dados: {err}", 'danger')
        return render_template('index.html', lista=[])
    finally:
        cursor.close()
        conexao.close()

    return render_template('index.html', lista=lista_times)


@app.route('/adicionar', methods=['POST'])
def adicionar_time():
    # Verifica se o usuário está logado
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado para adicionar um time.', 'warning')
        return redirect(url_for('login'))
    
    # Recupera os dados do formulário
    nome = request.form['nome']
    estado = request.form['estado']
    apelido = request.form['apelido']
    
    # Recupera o ID do usuário logado
    user_id = session.get('usuario_logado')

    # Verifica se o ID do usuário é válido
    if not user_id or not str(user_id).isdigit():
        flash('ID do usuário inválido. Tente fazer login.', 'danger')
        return redirect(url_for('cadastrar'))

    # Conexão com o banco de dados
    conexao = get_db_connection()
    cursor = conexao.cursor()

    try:
        # Insere um novo time no banco de dados com o ID do usuário logado
        cursor.execute(
            "INSERT INTO times (nome_time, estado_time, apelido_time, usuario_id_time) VALUES (%s, %s, %s, %s)",
            (nome, estado, apelido, user_id)
        )
        conexao.commit()
        flash('Time adicionado com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f"Erro ao adicionar time: {err}", 'danger')
    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for('cadastrar'))

@app.route('/editar/<int:id>', methods=['GET'])
def editar_time(id):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM times WHERE id_time = %s", (id,))
        time = cursor.fetchone()
        if not time:
            flash('Time não encontrado.', 'warning')
            return redirect(url_for('index'))
    except mysql.connector.Error as err:
        flash(f'Erro ao acessar o banco de dados: {err}', 'danger')
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conexao.close()

    return render_template('editar_time.html', time=time)

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar_time(id):
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado para atualizar um time.', 'warning')
        return redirect(url_for('login'))     
       
    nome = request.form['nome']
    estado = request.form['estado']
    apelido = request.form['apelido']
    user_id = session.get('usuario_logado')

    if not user_id or not str(user_id).isdigit():
        flash('ID do usuário inválido. Tente fazer login.', 'danger')
        return redirect(url_for('index'))

    conexao = get_db_connection()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "UPDATE times SET nome_time = %s, estado_time = %s, apelido_time = %s WHERE id_time = %s AND usuario_id_time = %s",
            (nome, estado, apelido, id, int(user_id))
        )
        conexao.commit()
        flash('Time atualizado com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f'Erro ao atualizar time: {err}', 'danger')
    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_time(id):
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado para deletar um time.', 'warning')
        return redirect(url_for('login'))
    
    user_id = session.get('usuario_logado')

    if not user_id or not str(user_id).isdigit():
        flash('ID do usuário inválido. Tente fazer login.', 'danger')
        return redirect(url_for('index'))
    
    conexao = get_db_connection()
    cursor = conexao.cursor()

    try:
        cursor.execute("DELETE FROM times WHERE id_time = %s AND usuario_id_time = %s", (id, int(user_id)))
        conexao.commit()
        flash('Time deletado com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f'Erro ao deletar time: {err}', 'danger')
    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for('index'))

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar_time.html')

@app.route('/login')
def login():
    if 'usuario_logado' in session:
        flash('Você já está logado.', 'info')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    login = request.form['login']
    senha = request.form['senha']

    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_usuario, nome_usuario, senha_usuario FROM usuarios WHERE nome_usuario = %s", (login,))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if usuario and check_password_hash(usuario[2], senha):
        session['usuario_logado'] = usuario[0] 
        flash(f'Bem-vindo(a), {usuario[1]}', 'success')
        return redirect(url_for('index'))
    else:
        flash('Usuário ou senha inválidos.', 'danger')
        return redirect(url_for('login'))

@app.route('/sair')
def sair():
    session.clear()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('login'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/criar_usuario', methods=['POST'])
def criar_usuario():
    nome = request.form['nome']
    senha = request.form['senha']

    senha_hash = generate_password_hash(senha)

    conexao = get_db_connection()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (nome_usuario, senha_usuario) VALUES (%s, %s)",
            (nome, senha_hash)
        )
        conexao.commit()
        flash('Usuário criado com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f'Erro ao criar usuário: {err}', 'danger')
    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)