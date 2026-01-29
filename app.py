from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "chave123"

# memória simples (funciona enquanto o app estiver rodando)
agendamentos = []

USUARIOS = {
    "aluno": "aluno123",
    "admin": "admin123"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["usuario"]
        s = request.form["senha"]

        if u in USUARIOS and USUARIOS[u] == s:
            session["usuario"] = u
            return redirect("/agendar" if u == "aluno" else "/admin")

        return render_template("login.html", erro=True)

    return render_template("login.html")


@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if session.get("usuario") != "aluno":
        return redirect("/")

    if request.method == "POST":
        agendamentos.append({
            "nome": request.form["nome"],
            "disciplina": request.form["disciplina"],
            "data": request.form["data"],
            "hora": request.form["hora"]
        })
        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")


@app.route("/admin")
def admin():
    if session.get("usuario") != "admin":
        return redirect("/")
    return render_template("admin.html", agendamentos=agendamentos)


@app.route("/sair")
def sair():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
