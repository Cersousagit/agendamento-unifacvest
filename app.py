from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "unifacvest123"

agendamentos = []

@app.route("/", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "admin" and senha == "Admin123":
            session["perfil"] = "admin"
            return redirect("/admin")

        elif senha == "Aluno123":
            session["perfil"] = "aluno"
            return redirect("/agendar")

        else:
            erro = "Usuário ou senha inválidos"

    return render_template("login.html", erro=erro)

@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if session.get("perfil") != "aluno":
        return redirect("/")

    msg = ""
    if request.method == "POST":
        agendamentos.append({
            "nome": request.form["nome"],
            "disciplinas": request.form["disciplinas"],
            "data": request.form["data"],
            "hora": request.form["hora"],
            "presente": False
        })
        msg = "Agendamento realizado com sucesso!"

    return render_template("agendar.html", msg=msg)

@app.route("/admin")
def admin():
    if session.get("perfil") != "admin":
        return redirect("/")

    hoje = datetime.now().strftime("%Y-%m-%d")

    ativos = []

    # garante que a lista exista
    global agendamentos
    if "agendamentos" not in globals():
        agendamentos = []

    for i, a in enumerate(agendamentos):
        if a.get("data", "") >= hoje:
            ativos.append({
                "index": i,
                "nome": a.get("nome", ""),
                "disciplinas": a.get("disciplinas", ""),
                "data": a.get("data", ""),
                "hora": a.get("hora", ""),
                "presente": a.get("presente", False)
            })

    return render_template("admin.html", agendamentos=ativos)

@app.route("/presente/<int:index>")
def marcar_presenca(index):
    if session.get("perfil") != "admin":
        return redirect("/")

    global agendamentos

    if index < len(agendamentos):
        agendamentos[index]["presente"] = True

    return redirect("/admin")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

