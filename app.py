from flask import Flask, render_template, redirect, request
import itertools

app = Flask(__name__)

agendamentos = []
contador_id = itertools.count(1)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def fazer_login():
    usuario = request.form["usuario"]
    senha = request.form["senha"]

    if usuario == "admin" and senha == "admin123":
        return redirect("/admin")
    elif senha == "aluno123":
        return redirect("/aluno")
    else:
        return redirect("/")

@app.route("/aluno")
def aluno():
    return render_template("agendar.html")

@app.route("/agendar", methods=["POST"])
def agendar():
    agendamentos.append({
        "id": next(contador_id),
        "nome": request.form["nome"],
        "disciplinas": request.form["disciplinas"],
        "data": request.form["data"],
        "hora": request.form["hora"],
        "presente": False
    })

    # ✅ mensagem de sucesso
    msg = "Agendamento realizado com sucesso!"

    return render_template("agendar.html", msg=msg)

@app.route("/admin")
def admin():
    total_presentes = sum(1 for a in agendamentos if a["presente"])
    return render_template(
        "admin.html",
        agendamentos=agendamentos,
        total_presentes=total_presentes
    )

@app.route("/presenca/<int:id>")
def presenca(id):
    for a in agendamentos:
        if a["id"] == id:
            a["presente"] = True
            break
    return redirect("/admin")

@app.route("/logout")
def logout():
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
