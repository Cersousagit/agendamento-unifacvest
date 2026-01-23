from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import os
from collections import Counter

app = Flask(__name__)
app.secret_key = "unifacvest123"

agendamentos = []

# ================= LOGIN =================
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
            return redirect("/agendar")

        else:
            erro = "Usuário ou senha inválidos"

    return render_template("login.html", erro=erro)


# ================= AGENDAR =================
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


# ================= ADMIN + DASHBOARD =================
@app.route("/admin")
def admin():
    if session.get("perfil") != "admin":
        return redirect("/")

    hoje = datetime.now().strftime("%Y-%m-%d")

    ativos = []
    datas = []
    presentes = 0
    pendentes = 0

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

            datas.append(a["data"])
            if a["presente"]:
                presentes += 1
            else:
                pendentes += 1

    contador_datas = Counter(datas)

    return render_template(
        "admin.html",
        agendamentos=ativos,
        total=len(ativos),
        presentes=presentes,
        pendentes=pendentes,
        datas=list(contador_datas.keys()),
        qtd_datas=list(contador_datas.values())
    )


# ================= PRESENÇA =================
@app.route("/presenca/<int:index>")
def presenca(index):
    if session.get("perfil") != "admin":
        return redirect("/")

    if index < len(agendamentos):
        agendamentos[index]["presente"] = True

    return redirect("/admin")


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
