from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "unifacvest123"

# Dados em memória
agendamentos = []

# Usuários fixos
usuarios = {
    "aluno": "aluno123",
    "admin": "admin123"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario in usuarios and usuarios[usuario] == senha:
            session["usuario"] = usuario

            if usuario == "aluno":
                return redirect("/agendar")
            else:
                return redirect("/admin")

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")


@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if "usuario" not in session or session["usuario"] != "aluno":
        return redirect("/")

    if request.method == "POST":
        agendamentos.append({
            "nome": request.form["nome"],
            "curso": request.form["curso"],
            "data": request.form["data"],
            "horario": request.form["horario"]
        })

        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")


@app.route("/admin")
def admin():
    if "usuario" not in session or session["usuario"] != "admin":
        return redirect("/")

    return render_template("admin.html", agendamentos=agendamentos)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
