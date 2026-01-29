from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "segredo"

# armazenamento temporário
agendamentos = []
confirmadas = 0

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
        agendamentos.append({
            "nome": request.form["nome"],
            "disciplinas": request.form.getlist("disciplinas[]"),
            "data": request.form["data"],
            "hora": request.form["hora"]
        })
        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")

@app.route("/admin")
def admin():
    if session.get("perfil") != "admin":
        return redirect("/")

    ordenado = sorted(
        agendamentos,
        key=lambda x: (x["data"], x["hora"])
    )

    return render_template(
        "admin.html",
        agendamentos=ordenado,
        total=len(ordenado),
        confirmadas=confirmadas
    )

@app.route("/confirmar/<int:index>")
def confirmar(index):
    global confirmadas
    if session.get("perfil") != "admin":
        return redirect("/")

    if index < len(agendamentos):
        agendamentos.pop(index)
        confirmadas += 1

    return redirect("/admin")

@app.route("/logout")
def logout():
    session.clear()
    agendamentos.clear()
    return redirect("/")
