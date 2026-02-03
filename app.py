from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "unifacvest123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        # LOGIN ADMIN
        if usuario == "admin" and senha == "admin123":
            session["usuario"] = "admin"
            return redirect("/admin")

        # LOGIN ALUNO
        elif usuario == "aluno" and senha == "aluno123":
            session["usuario"] = "aluno"
            return redirect("/agendamento")

        else:
            return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")
