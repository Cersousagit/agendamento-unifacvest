from flask import Flask, render_template, redirect, url_for, request, send_file
from datetime import date, datetime
import itertools
from openpyxl import Workbook

app = Flask(__name__)

agendamentos = []
contador_id = itertools.count(1)

# ================= LOGIN =================
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
    return redirect("/")

# ================= ALUNO =================
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
    return render_template("agendar.html", msg="Agendamento realizado com sucesso")

# ================= ADMIN =================
@app.route("/admin")
def admin():
    hoje = date.today().isoformat()

    # Filtros
    mes = request.args.get("mes")
    ano = request.args.get("ano")

    registros = [a for a in agendamentos if a["data"] >= hoje]

    if mes and ano:
        registros = [
            a for a in registros
            if a["data"][5:7] == mes and a["data"][:4] == ano
        ]

    registros.sort(key=lambda x: (x["data"], x["hora"]))

    total_presentes = sum(1 for a in registros if a["presente"])
    total_faltas = sum(1 for a in registros if not a["presente"])

    return render_template(
        "admin.html",
        agendamentos=registros,
        total_presentes=total_presentes,
        total_faltas=total_faltas,
        mes=mes,
        ano=ano
    )

# ================= PRESENÇA =================
@app.route("/presenca/<int:id>")
def presenca(id):
    for a in agendamentos:
        if a["id"] == id:
            a["presente"] = True
            break
    return redirect("/admin")

# ================= RELATÓRIO EXCEL =================
@app.route("/relatorio-excel")
def relatorio_excel():
    mes = request.args.get("mes")
    ano = request.args.get("ano")

    wb = Workbook()
    ws = wb.active
    ws.title = "Relatório"

    ws.append(["Aluno", "Disciplinas", "Data", "Hora", "Status"])

    registros = agendamentos

    if mes and ano:
        registros = [
            a for a in registros
            if a["data"][5:7] == mes and a["data"][:4] == ano
        ]

    registros.sort(key=lambda x: (x["data"], x["hora"]))

    for a in registros:
        ws.append([
            a["nome"],
            a["disciplinas"],
            datetime.strptime(a["data"], "%Y-%m-%d").strftime("%d/%m/%Y"),
            a["hora"],
            "Presente" if a["presente"] else "Falta"
        ])

    nome = f"relatorio_{mes or 'todos'}_{ano or 'anos'}.xlsx"
    caminho = f"/tmp/{nome}"
    wb.save(caminho)

    return send_file(caminho, as_attachment=True, download_name=nome)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
