from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date

app = Flask(__name__)
app.secret_key = "chave_secreta_segura"

provas = []

# ======================
# LOGIN PADRÃO (ALUNO)
# ======================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/agendar")
    return render_template("login.html")

# ======================
# AGENDAMENTO
# ======================
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
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
# LOGIN ADMIN
# ======================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    erro = ""
    if request.method == "POST":
        if request.form["usuario"] == "admin" and request.form["senha"] == "1234":
            session["admin"] = True
            return redirect("/admin")
        else:
            erro = "Usuário ou senha inválidos"
    return render_template("admin_login.html", erro=erro)

# ======================
# DASHBOARD ADMIN
# ======================
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin/login")

    hoje = date.today().isoformat()
    provas_validas = [p for p in provas if p["data"] >= hoje]

    total_presencas = sum(1 for p in provas if p["presenca"] == "Presente")

    return render_template(
        "admin.html",
        provas=provas_validas,
        total=total_presencas
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
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/admin/login")

if __name__ == "__main__":
    app.run(debug=True)
