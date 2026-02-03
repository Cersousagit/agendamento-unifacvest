from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "unifacvest-secret"

# BASE EM MEMÓRIA (simples e estável)
agendamentos = []
contador_id = 1


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


@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    global contador_id

    if session.get("usuario") != "aluno":
        return redirect("/")

    if request.method == "POST":
        agendamentos.append({
            "id": contador_id,
            "nome": request.form["nome"],
            "disciplina": request.form["disciplina"],
            "data": request.form["data"],
            "hora": request.form["hora"],
            "status": "pendente"
        })
        contador_id += 1
        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")


@app.route("/admin")
def admin():
    if session.get("usuario") != "admin":
        return redirect("/")

    pendentes = [a for a in agendamentos if a["status"] == "pendente"]
    confirmadas = [a for a in agendamentos if a["status"] == "confirmada"]

    return render_template("admin.html",
                           pendentes=pendentes,
                           confirmadas=confirmadas)


@app.route("/confirmar/<int:id>")
def confirmar(id):
    if session.get("usuario") != "admin":
        return redirect("/")

    for a in agendamentos:
        if a["id"] == id:
            a["status"] = "confirmada"
            break
    return redirect("/admin")


@app.route("/presenca/<int:id>")
def presenca(id):
    if session.get("usuario") != "admin":
        return redirect("/")

    global agendamentos
    agendamentos = [a for a in agendamentos if a["id"] != id]

    return redirect("/admin")


@app.route("/sair")
def sair():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
