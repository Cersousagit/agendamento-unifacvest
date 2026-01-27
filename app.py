from flask import Flask, render_template, redirect, url_for, request
from datetime import date
import itertools

app = Flask(__name__)

# Banco simples em memória
agendamentos = []
contador_id = itertools.count(1)

# ======================
# LOGIN
# ======================
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
        return redirect("/aluno")
    else:
        return redirect("/")

# ======================
# ALUNO
# ======================
@app.route("/aluno")
def aluno():
    return render_template("agendar.html")

@app.route("/agendar", methods=["POST"])
def agendar():
    agendamentos.append({
        "id": next(contador_id),
        "nome": request.form["nome"],
        "disciplinas": request.form["disciplinas"],
        "data": request.form["data"],
        "hora": request.form["hora"],
        "presente": False
    })

    return render_template(
        "agendar.html",
        msg="Agendamento realizado com sucesso"
    )

# ======================
# ADMIN
# ======================
@app.route("/admin")
def admin():
    hoje = date.today().isoformat()

    # 🔥 REMOVE PROVAS COM DATA PASSADA
    agendamentos_validos = [
        a for a in agendamentos if a["data"] >= hoje
    ]

    # Ordenar por data + hora
    agendamentos_validos.sort(
        key=lambda x: (x["data"], x["hora"])
    )

    total_presentes = sum(
        1 for a in agendamentos_validos if a["presente"]
    )

    return render_template(
        "admin.html",
        agendamentos=agendamentos_validos,
        total_presentes=total_presentes
    )

# ======================
# PRESENÇA
# ======================
@app.route("/presenca/<int:id>")
def presenca(id):
    for a in agendamentos:
        if a["id"] == id:
            a["presente"] = True
            break
    return redirect("/admin")

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
