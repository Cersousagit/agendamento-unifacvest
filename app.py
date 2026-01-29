from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "segredo"

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

    if "agendamentos" not in session:
        session["agendamentos"] = []

    if request.method == "POST":
        session["agendamentos"].append({
            "nome": request.form["nome"],
            "disciplinas": request.form.getlist("disciplinas[]"),
            "data": request.form["data"],
            "hora": request.form["hora"]
        })
        session.modified = True
        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")


@app.route("/admin")
def admin():
    if session.get("perfil") != "admin":
        return redirect("/")

    ag = session.get("agendamentos", [])
    confirmadas = session.get("confirmadas", 0)

    ag = sorted(ag, key=lambda x: (x["data"], x["hora"]))

    return render_template(
        "admin.html",
        agendamentos=ag,
        total=len(ag),
        confirmadas=confirmadas
    )


@app.route("/confirmar/<int:index>")
def confirmar(index):
    if session.get("perfil") != "admin":
        return redirect("/")

    if "agendamentos" in session and index < len(session["agendamentos"]):
        session["agendamentos"].pop(index)
        session["confirmadas"] = session.get("confirmadas", 0) + 1
        session.modified = True

    return redirect("/admin")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
