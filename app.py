from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'chave-secreta'

# Banco em memória
provas = []
contador_id = 1

# LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['senha'] == 'admin':
            session['user'] = 'admin'
            return redirect('/admin')
    return render_template('login.html')


# AGENDAMENTO DO ALUNO
@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    global contador_id

    if request.method == 'POST':
        nova_prova = {
            'id': contador_id,
            'nome': request.form['nome'],
            'disciplinas': request.form['disciplina'],
            'data': request.form['data'],
            'hora': request.form['hora'],
            'confirmado': True
        }
        provas.append(nova_prova)
        contador_id += 1
        return redirect('/agendar')

    return render_template('agendamento.html')


# PAINEL ADMIN
@app.route('/admin')
def admin():
    if session.get('user') != 'admin':
        return redirect('/')

    pendentes = [p for p in provas if not p['confirmado']]
    confirmadas = [p for p in provas if p['confirmado']]

    return render_template(
        'admin.html',
        pendentes=pendentes,
        confirmadas=confirmadas
    )


# CONFIRMAR PRESENÇA (REMOVE DEFINITIVAMENTE)
@app.route('/presenca/<int:id>')
def presenca(id):
    if session.get('user') != 'admin':
        return redirect('/')

    global provas
    provas = [p for p in provas if p['id'] != id]

    return redirect('/admin')


# SAIR
@app.route('/sair')
def sair():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
