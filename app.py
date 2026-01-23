from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "unifacvest123"

agendamentos = []

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()

        # ADMIN / POLO
        if usuario == "admin" and senha == "admin123":
            session["perfil"] = "admin"
            return redirect("/admin")

        # ALUNO
        elif usuario != "" and senha == "aluno123":
            session["perfil"] = "aluno"
            session["nome_aluno"] = usuario
            return redirect("/agendar")

        else:
            erro = "Credenciais inválidas"

    return render_template("login.html", erro=erro)


# ================= AGENDAMENTO ALUNO =================
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if session.get("perfil") != "aluno":
        return redirect("/")

    msg = ""

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        disciplinas = request.form.get("disciplinas", "").strip()
        data = request.form.get("data", "").strip()
        hora = request.form.get("hora", "").strip()

        # VALIDAÇÃO OBRIGATÓRIA
        if not nome or not disciplinas or not data or not hora:
            msg = "❌ Todos os campos são obrigatórios"
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


# ================= ADMIN =================
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


# ================= PRESENÇA =================
@app.route("/presenca/<int:index>")
def marcar_presenca(index):
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
