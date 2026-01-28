from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "chave_secreta"

# ======================
# DADOS EM MEMÓRIA
# ======================
agendamentos = []

# ======================
# LOGIN ALUNO
# ======================
@app.route("/", methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        if request.form["usuario"] == "aluno" and request.form["senha"] == "aluno123":
            session["aluno"] = True
            return redirect("/agendar")
        else:
            erro = "Login inválido"
    return render_template("login.html", erro=erro)

# ======================
# AGENDAMENTO ALUNO
# ======================
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if not session.get("aluno"):
        return redirect("/")

    if request.method == "POST":
        agendamentos.append({
            "nome": request.form["nome"],
            "disciplina": request.form["disciplina"],
            "data": request.form["data"],
            "hora": request.form["hora"],
            "status": "Pendente"
        })

    return render_template("agendar.html")

# ======================
# LOGIN + PAINEL ADMIN
# ======================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    erro = ""

    if request.method == "POST":
        if request.form["usuario"] == "admin" and request.form["senha"] == "admin123":
            session["admin"] = True
        else:
            erro = "Login inválido"

    if not session.get("admin"):
        return render_template("admin.html", login=True, erro=erro, agendamentos=[])

    return render_template(
        "admin.html",
        login=False,
        agendamentos=agendamentos
    )

# ======================
# CONFIRMAR PRESENÇA
# ======================
@app.route("/confirmar/<int:i>/<status>")
def confirmar(i, status):
    if session.get("admin"):
        agendamentos[i]["status"] = status
    return redirect("/admin")

# ======================
# LOGOUTS
# ======================
@app.route("/sair")
def sair():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
