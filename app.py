from flask import Flask, render_template, request, redirect, session, url_for
from datetime import date

app = Flask(__name__)
app.secret_key = "segredo_seguro"

# ======================
# DADOS EM MEMÓRIA
# ======================
provas = []

# ======================
# LOGIN ALUNO
# ======================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["aluno"] = request.form["nome"]
        return redirect("/agendar")
    return render_template("login.html")

# ======================
# AGENDAMENTO ALUNO
# ======================
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if "aluno" not in session:
        return redirect("/")

    msg = ""
    if request.method == "POST":
        provas.append({
            "nome": request.form["nome"],
            "disciplinas": request.form.getlist("disciplinas[]"),
            "data": request.form["data"],
            "hora": request.form["hora"],
            "presenca": None
        })
        msg = "Agendamento realizado com sucesso"

    return render_template("agendar.html", msg=msg)

# ======================
# LOGIN ADMIN (POLO)
# ======================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["usuario"] == "admin" and request.form["senha"] == "1234":
            session["admin"] = True
        else:
            return render_template("admin.html", erro="Login inválido", provas=[])

    if not session.get("admin"):
        return render_template("admin.html", provas=[], login=True)

    hoje = date.today().isoformat()
    provas_ativas = [p for p in provas if p["data"] >= hoje]

    total = sum(1 for p in provas if p["presenca"] == "Presente")

    return render_template(
        "admin.html",
        provas=provas_ativas,
        total=total,
        login=False
    )

# ======================
# CONFIRMAR PRESENÇA
# ======================
@app.route("/confirmar/<int:i>/<status>")
def confirmar(i, status):
    if session.get("admin"):
        provas[i]["presenca"] = status
    return redirect("/admin")

# ======================
# SAIR ADMIN
# ======================
@app.route("/admin/sair")
def sair_admin():
    session.pop("admin", None)
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)
