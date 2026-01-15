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
    ativos = [a for a in agendamentos if a["data"] >= hoje]
    return render_template("admin.html", agendamentos=ativos)

@app.route("/presenca/<int:index>")
def presenca(index):
    if session.get("perfil") == "admin":
        agendamentos[index]["presente"] = True
    return redirect("/admin")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
