from flask import Flask, render_template, redirect, url_for, request
import itertools
import os

app = Flask(__name__)

agendamentos = []
contador_id = itertools.count(1)

# LOGIN
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

# ALUNO / AGENDAMENTO
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    msg = None

    if request.method == "POST":
        agendamentos.append({
            "id": next(contador_id),
            "nome": request.form["nome"],
            "disciplinas": request.form["disciplinas"],
            "data": request.form["data"],
            "hora": request.form["hora"],
            "presente": False
        })
        msg = "✅ Prova agendada com sucesso!"

    return render_template("agendar.html", msg=msg)

# ADMIN
@app.route("/admin")
def admin():
    total_presentes = sum(1 for a in agendamentos if a["presente"])
    return render_template(
        "admin.html",
        agendamentos=agendamentos,
        total_presentes=total_presentes
    )

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

# ⚠️ NÃO USAR app.run() NO RENDER
