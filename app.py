from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "unifacvest123"

agendamentos = []

USUARIOS = {
    "aluno": {"senha": "aluno123", "tipo": "aluno"},
    "admin": {"senha": "admin123", "tipo": "admin"}
}

@app.route("/", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
            session["usuario"] = usuario
            session["tipo"] = USUARIOS[usuario]["tipo"]

            if session["tipo"] == "aluno":
                return redirect(url_for("agendar"))
            else:
                return redirect(url_for("admin"))
        else:
            erro = "Usuário ou senha inválidos"

    return render_template("login.html", erro=erro)

@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if "usuario" not in session or session["tipo"] != "aluno":
        return redirect(url_for("login"))

    sucesso = False

    if request.method == "POST":
        nome = request.form["nome"]
        disciplinas = request.form.getlist("disciplinas[]")
        data = request.form["data"]
        hora = request.form["hora"]

        agendamentos.append({
            "nome": nome,
            "disciplinas": disciplinas,
            "data": data,
            "hora": hora
        })

        sucesso = True

    return render_template("agendar.html", sucesso=sucesso)

@app.route("/admin")
def admin():
    if "usuario" not in session or session["tipo"] != "admin":
        return redirect(url_for("login"))

    return render_template("admin.html", agendamentos=agendamentos)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
