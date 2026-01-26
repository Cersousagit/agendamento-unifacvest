from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import itertools

app = Flask(__name__, template_folder="modelos")
app.secret_key = "unifacvest123"

agendamentos = []
contador_id = itertools.count(1)

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        nome = request.form.get("nome", "")

        if usuario == "admin" and senha == "admin123":
            session["perfil"] = "admin"
            return redirect("/admin")

        elif senha == "aluno123" and nome.strip() != "":
            session["perfil"] = "aluno"
            session["nome"] = nome
            return redirect("/agendar")

        else:
            erro = "Dados inválidos"

    return render_template("login.html", erro=erro)

# ---------- AGENDAR ----------
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if session.get("perfil") != "aluno":
        return redirect("/")

    msg = ""
    if request.method == "POST":
        agendamentos.append({
            "id": next(contador_id),
            "nome": session["nome"],
            "disciplinas": request.form["disciplinas"],
            "data": request.form["data"],
            "hora": request.form["hora"],
            "presente": False
        })
        msg = "Agendamento realizado com sucesso!"

    return render_template("agendar.html", msg=msg)

# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    if session.get("perfil") != "admin":
        return redirect("/")

    total_presentes = sum(1 for a in agendamentos if a["presente"])

    datas = []
    quantidades = []

    for a in agendamentos:
        if a["data"] not in datas:
            datas.append(a["data"])
            quantidades.append(1)
        else:
            idx = datas.index(a["data"])
            quantidades[idx] += 1

    return render_template(
        "admin.html",
        agendamentos=agendamentos,
        total_presentes=total_presentes,
        datas=datas,
        quantidades=quantidades
    )

# ---------- PRESENÇA ----------
@app.route("/presenca/<int:id>")
def presenca(id):
    if session.get("perfil") != "admin":
        return redirect("/")

    for a in agendamentos:
        if a["id"] == id:
            a["presente"] = True
            break

    return redirect(url_for("admin"))

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
