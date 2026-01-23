from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "unifacvest123"

agendamentos = []

@app.route("/", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        senha = request.form["senha"].strip()

        if usuario == "admin" and senha == "admin123":
            session["perfil"] = "admin"
            return redirect("/admin")

        elif usuario != "" and senha == "aluno123":
            session["perfil"] = "aluno"
            session["nome"] = usuario
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
        nome = request.form["nome"]
        disciplinas = request.form["disciplinas"]
        data = request.form["data"]
        hora = request.form["hora"]

        if not nome or not disciplinas or not data or not hora:
            msg = "❌ Preencha todos os campos"
        else:
            agendamentos.append({
                "nome": nome,
                "disciplinas": disciplinas,
                "data": data,
                "hora": hora,
                "presente": False
            })
            msg = "✅ Agendamento realizado com sucesso!"

    return render_template("agendar.html", msg=msg)


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


@app.route("/presenca/<int:index>")
def presenca(index):
    if session.get("perfil") != "admin":
        return redirect("/")

    if index < len(agendamentos):
        agendamentos[index]["presente"] = True

    return redirect("/admin")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
