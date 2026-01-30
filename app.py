from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "segredo_unifacvest"

# usuários fixos
USUARIOS = {
    "aluno": "aluno123",
    "admin": "admin123"
}

# armazenamento em memória (simples e funcional)
agendamentos = []
contador_id = 1


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            session["usuario"] = usuario
            if usuario == "admin":
                return redirect("/admin")
            return redirect("/agendar")

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")


@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    global contador_id

    if "usuario" not in session or session["usuario"] != "aluno":
        return redirect("/")

    if request.method == "POST":
        nome = request.form["nome"]
        data = request.form["data"]
        hora = request.form["hora"]
        disciplina = request.form["disciplina"]

        agendamentos.append({
            "id": contador_id,
            "nome": nome,
            "disciplina": disciplina,
            "data": data,
            "hora": hora,
            "status": "pendente"
        })
        contador_id += 1

        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")


@app.route("/admin")
def admin():
    if "usuario" not in session or session["usuario"] != "admin":
        return redirect("/")

    pendentes = [a for a in agendamentos if a["status"] == "pendente"]
    confirmadas = [a for a in agendamentos if a["status"] == "confirmada"]

    # ordenar por data e hora
    pendentes.sort(key=lambda x: (x["data"], x["hora"]))
    confirmadas.sort(key=lambda x: (x["data"], x["hora"]))

    return render_template(
        "admin.html",
        pendentes=pendentes,
        confirmadas=confirmadas
    )


@app.route("/confirmar/<int:id>")
def confirmar(id):
    for a in agendamentos:
        if a["id"] == id:
            a["status"] = "confirmada"
            break
    return redirect("/admin")


@app.route("/sair")
def sair():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
