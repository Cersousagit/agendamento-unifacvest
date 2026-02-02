from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'segredo123'

# ==========================
# "BANCO DE DADOS" SIMPLES
# ==========================
provas = []
contador_id = 1

# ==========================
# LOGIN
# ==========================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario == 'aluno' and senha == 'aluno123':
            session['user'] = 'aluno'
            return redirect('/agendar')

        if usuario == 'admin' and senha == 'admin123':
            session['user'] = 'admin'
            return redirect('/admin')

        return render_template('login.html', erro='Usuário ou senha inválidos')

    return render_template('login.html')


# ==========================
# AGENDAMENTO (ALUNO)
# ==========================
@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    global contador_id

    if session.get('user') != 'aluno':
        return redirect('/')

    if request.method == 'POST':
        prova = {
            'id': contador_id,
            'nome': request.form['nome'],
            'disciplinas': request.form['disciplinas'],
            'data': request.form['data'],
            'hora': request.form['hora'],
            'status': 'pendente',
            'presente': False
        }
        provas.append(prova)
        contador_id += 1

        return render_template('agendar.html', sucesso=True)

    return render_template('agendar.html')


# ==========================
# ADMIN
# ==========================
@app.route('/admin')
def admin():
    if session.get('user') != 'admin':
        return redirect('/')

    pendentes = [p for p in provas if p['status'] == 'pendente']
    confirmadas = [p for p in provas if p['status'] == 'confirmada']

    return render_template(
        'admin.html',
        pendentes=pendentes,
        confirmadas=confirmadas
    )


# ==========================
# CONFIRMAR PROVA
# ==========================
@app.route('/confirmar/<int:id>')
def confirmar(id):
    if session.get('user') != 'admin':
        return redirect('/')

    for p in provas:
        if p['id'] == id:
            p['status'] = 'confirmada'
            break

    return redirect('/admin')


# ==========================
# MARCAR PRESENÇA  ✅ (AQUI ESTAVA O ERRO)
# ==========================
@app.route('/presenca/<int:id>')
def presenca(id):
    if session.get('user') != 'admin':
        return redirect('/')

    for p in provas:
        if p['id'] == id:
            p['presente'] = True
            break

    return redirect('/admin')


# ==========================
# SAIR
# ==========================
@app.route('/sair')
def sair():
    session.clear()
    return redirect('/')


# ==========================
if __name__ == '__main__':
    app.run(debug=True)
