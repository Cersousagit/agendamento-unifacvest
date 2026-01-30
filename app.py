from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "unifacvest123"

# armazenamento simples (sem banco, mas funcional)
agendamentos = []


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
    if "usuario" not in session or session["usuario"] != "aluno":
        return redirect("/")

    if request.method == "POST":
        nome = request.form.get("nome")
        disciplinas = request.form.get("disciplinas")
        data = request.form.get("data")
        hora = request.form.get("hora")

        if not nome or not disciplinas or not data or not hora:
            return "Erro: dados incompletos", 400

        agendamentos.append({
            "nome": nome,
            "disciplinas": disciplinas,
            "data": data,
            "hora": hora,
            "status": "confirmado"
        })

        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")


# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    if "usuario" not in session or session["usuario"] != "admin":
        return redirect("/")

    confirmados = sorted(
        agendamentos,
        key=lambda x: (x["data"], x["hora"])
    )

    return render_template(
        "admin.html",
        confirmados=confirmados,
        total=len(confirmados)
    )


# ---------- SAIR ----------
@app.route("/sair")
def sair():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
