from flask import Flask, render_template, request, redirect, session, url_for
import json
import os

app = Flask(__name__)
app.secret_key = "unifacvest-secret"

# Persistência simples com JSON (funciona no Render, mas não escalável)
DATA_FILE = 'agendamentos.json'

def load_agendamentos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_agendamentos(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

agendamentos = load_agendamentos()
contador_id = max([a.get('id', 0) for a in agendamentos], default=0) + 1

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario == "admin" and senha == "admin123":
            session["usuario"] = "admin"
            return redirect("/admin")
        if usuario == "aluno" and senha == "aluno123":
            session["usuario"] = "aluno"
            return redirect("/agendar")

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")

@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    global contador_id, agendamentos

    if session.get("usuario") != "aluno":
        return redirect("/")

    if request.method == "POST":
        try:
            novo = {
                "id": contador_id,
                "nome": request.form["nome"],
                "disciplina": request.form["disciplina"],
                "data": request.form["data"],
                "hora": request.form["hora"],
                "status": "pendente"
            }
            agendamentos.append(novo)
            save_agendamentos(agendamentos)
            contador_id += 1
            return render_template("agendar.html", sucesso=True)
        except KeyError:
            return render_template("agendar.html", erro="Dados inválidos")

    return render_template("agendar.html")

@app.route("/admin")
def admin():
    if session.get("usuario") != "admin":
        return redirect("/")

    pendentes = [a for a in agendamentos if a["status"] == "pendente"]
    confirmadas = [a for a in agendamentos if a["status"] == "confirmada"]

    return render_template("admin.html", pendentes=pendentes, confirmadas=confirmadas)

@app.route("/confirmar/<int:id>")
def confirmar(id):
    if session.get("usuario") != "admin":
        return redirect("/")

    for a in agendamentos:
        if a["id"] == id:
            a["status"] = "confirmada"
            save_agendamentos(agendamentos)
            break
    return redirect("/admin")

@app.route("/presenca/<int:id>")
def presenca(id):
    if session.get("usuario") != "admin":
        return redirect("/")

    for a in agendamentos:
        if a["id"] == id:
            a["status"] = "presenca_confirmada"  # Marca em vez de deletar
            save_agendamentos(agendamentos)
            break
    return redirect("/admin")

@app.route("/sair")
def sair():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
