from flask import Flask, render_template, redirect, url_for, request
import itertools

app = Flask(__name__)

agendamentos = []
contador_id = itertools.count(1)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def fazer_login():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    if usuario == "admin" and senha == "admin123":
        return redirect("/admin")
    elif senha == "aluno123":
        return redirect("/agendar")
    else:
        return redirect("/")

@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    msg = None

    if request.method == "POST":
        disciplinas_lista = request.form.getlist("disciplinas[]")
        disciplinas = ", ".join(disciplinas_lista)

        agendamentos.append({
            "id": next(contador_id),
            "nome": request.form.get("nome"),
            "disciplinas": disciplinas,
            "data": request.form.get("data"),
            "hora": request.form.get("hora"),
            "presente": False
        })

        msg = "Prova agendada com sucesso!"

    return render_template("agendar.html", msg=msg)


@app.route("/admin")
def admin():
    total = len(agendamentos)
    presentes = sum(1 for a in agendamentos if a["presente"])
    ausentes = total - presentes

    return render_template(
        "admin.html",
        agendamentos=agendamentos,
        total=total,
        presentes=presentes,
        ausentes=ausentes
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
    app.run(host="0.0.0.0", port=5000)
