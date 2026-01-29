from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "segredo"

ARQ = "agendamentos.json"

def ler_agendamentos():
    if not os.path.exists(ARQ):
        return []
    with open(ARQ, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_agendamentos(lista):
    with open(ARQ, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["usuario"]
        s = request.form["senha"]

        if u == "aluno" and s == "aluno123":
            session["perfil"] = "aluno"
            return redirect("/agendar")

        if u == "admin" and s == "admin123":
            session["perfil"] = "admin"
            return redirect("/admin")

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")


@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if session.get("perfil") != "aluno":
        return redirect("/")

    if request.method == "POST":
        ag = ler_agendamentos()

        ag.append({
            "nome": request.form["nome"],
            "disciplinas": request.form.getlist("disciplinas[]"),
            "data": request.form["data"],
            "hora": request.form["hora"],
            "status": "pendente"
        })

        salvar_agendamentos(ag)
        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")


@app.route("/admin")
def admin():
    if session.get("perfil") != "admin":
        return redirect("/")

    ag = ler_agendamentos()
    pendentes = [a for a in ag if a["status"] == "pendente"]
    confirmadas = [a for a in ag if a["status"] == "confirmada"]

    pendentes.sort(key=lambda x: (x["data"], x["hora"]))

    return render_template(
        "admin.html",
        pendentes=pendentes,
        total_p=len(pendentes),
        total_c=len(confirmadas)
    )


@app.route("/confirmar/<int:i>")
def confirmar(i):
    if session.get("perfil") != "admin":
        return redirect("/")

    ag = ler_agendamentos()
    if i < len(ag):
        ag[i]["status"] = "confirmada"
        salvar_agendamentos(ag)

    return redirect("/admin")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
