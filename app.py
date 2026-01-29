from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "segredo123"

# Banco de dados simples em memória
agendamentos = []

# Usuários fixos
USUARIOS = {
    "aluno": "aluno123",
    "admin": "admin123"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            session["usuario"] = usuario

            if usuario == "aluno":
                return redirect(url_for("agendar"))
            else:
                return redirect(url_for("admin"))

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")


@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if "usuario" not in session or session["usuario"] != "aluno":
        return redirect(url_for("login"))

    if request.method == "POST":
        nome = request.form["nome"]
        curso = request.form["curso"]
        data = request.form["data"]
        horario = request.form["horario"]

        agendamentos.append({
            "nome": nome,
            "curso": curso,
            "data": data,
            "horario": horario
        })

        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")


@app.route("/admin")
def admin():
    if "usuario" not in session or session["usuario"] != "admin":
        return redirect(url_for("login"))

    return render_template("admin.html", agendamentos=agendamentos)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
