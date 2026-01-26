from flask import Flask, render_template, redirect, request
import itertools

app = Flask(__name__)
app.secret_key = "unifacvest"

# Banco de dados em memória
agendamentos = []
contador_id = itertools.count(1)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def fazer_login():
    usuario = request.form["usuario"]
    senha = request.form["senha"]

    if usuario == "admin" and senha == "admin123":
        return redirect("/admin")
    elif senha == "aluno123":
        return redirect("/agendar")
    else:
        return redirect("/")

@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    msg = ""
    if request.method == "POST":
        agendamentos.append({
            "id": next(contador_id),
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
    return render_template("admin.html", agendamentos=agendamentos)

@app.route("/presenca/<int:id>")
def presenca(id):
    for a in agendamentos:
        if a["id"] == id:
            a["presente"] = True
            break
    return redirect("/admin")

@app.route("/logout")
def logout():
    return redirect("/")
