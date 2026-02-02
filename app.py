from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "unifacvest123"

ARQUIVO = "agendamentos.json"


# ---------- UTIL ----------
def carregar_agendamentos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_agendamentos(lista):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)


# ---------- LOGIN ----------
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


# ---------- AGENDAR ----------
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if session.get("usuario") != "aluno":
        return redirect("/")

    if request.method == "POST":
        nome = request.form.get("nome")
        disciplinas = request.form.get("disciplinas")
        data = request.form.get("data")
        hora = request.form.get("hora")

        if not all([nome, disciplinas, data, hora]):
            return "Erro: dados incompletos", 400

        agendamentos = carregar_agendamentos()

        agendamentos.append({
            "nome": nome,
            "disciplinas": disciplinas,
            "data": data,
            "hora": hora,
            "status": "confirmado"
        })

        salvar_agendamentos(agendamentos)

        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")


# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    if session.get("usuario") != "admin":
        return redirect("/")

    agendamentos = carregar_agendamentos()

    confirmadas = sorted(
        [a for a in agendamentos if a["status"] == "confirmado"],
        key=lambda x: (x["data"], x["hora"])
    )

    return render_template(
        "admin.html",
        confirmadas=confirmadas,
        total=len(confirmadas)
    )


# ---------- SAIR ----------
@app.route("/sair")
def sair():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
