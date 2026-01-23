from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "unifacvest123"

agendamentos = []

# LOGIN
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


# ALUNO
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


# ADMIN
@app.route("/admin")
def admin():
    if session.get("perfil") != "admin":
        return redirect("/")

    hoje = datetime.now().strftime("%Y-%m-%d")
    ativos = []

    for i, a in enumerate(agendamentos):
        if a["data"] >= hoje:
            ativos.append({
                "index": i,
                "nome": a["nome"],
                "disciplinas": a["disciplinas"],
                "data": a["data"],
                "hora": a["hora"],
                "presente": a["presente"]
            })

    return render_template("admin.html", agendamentos=ativos)


# ✅ MARCAR PRESENÇA (ROTA CORRETA)
@app.route("/presenca/<int:index>")
def marcar_presenca(index):
    if session.get("perfil") != "admin":
        return redirect("/")

    if index < len(agendamentos):
        agendamentos[index]["presente"] = True

    return redirect("/admin")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
