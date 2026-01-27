from flask import Flask, render_template, request, redirect, url_for, send_file
from datetime import datetime
import openpyxl
import io

app = Flask(__name__)

# armazenamento simples (memória)
agendamentos = []

# -------------------------
# TELA DO ALUNO
# -------------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    mensagem = None

    if request.method == "POST":
        nome = request.form.get("nome")
        disciplinas = request.form.getlist("disciplinas[]")
        data = request.form.get("data")
        hora = request.form.get("hora")

        if not nome or not disciplinas or not data or not hora:
            return "Bad Request", 400

        agendamentos.append({
            "nome": nome,
            "disciplinas": disciplinas,
            "data": data,
            "hora": hora,
            "presente": False
        })

        mensagem = "Agendamento realizado com sucesso"

    return render_template("agendar.html", mensagem=mensagem)

# -------------------------
# ADMIN
# -------------------------
@app.route("/admin")
def admin():
    hoje = datetime.now().date()

    provas_validas = [
        p for p in agendamentos
        if datetime.strptime(p["data"], "%Y-%m-%d").date() >= hoje
    ]

    provas_validas.sort(key=lambda p: (p["data"], p["hora"]))

    mes_selecionado = request.args.get("mes", "")
    ano_selecionado = request.args.get("ano", "")

    if mes_selecionado:
        provas_validas = [p for p in provas_validas if p["data"].split("-")[1] == mes_selecionado]

    if ano_selecionado:
        provas_validas = [p for p in provas_validas if p["data"].split("-")[0] == ano_selecionado]

    meses = sorted({p["data"].split("-")[1] for p in agendamentos})
    anos = sorted({p["data"].split("-")[0] for p in agendamentos})

    total_presencas = sum(1 for p in provas_validas if p["presente"])
    total_faltas = sum(1 for p in provas_validas if not p["presente"])

    return render_template(
        "admin.html",
        provas=provas_validas,
        meses=meses,
        anos=anos,
        mes_selecionado=mes_selecionado,
        ano_selecionado=ano_selecionado,
        total_presencas=total_presencas,
        total_faltas=total_faltas
    )

# -------------------------
# MARCAR PRESENÇA
# -------------------------
@app.route("/presenca/<int:index>")
def marcar_presenca(index):
    if 0 <= index < len(agendamentos):
        agendamentos[index]["presente"] = True
    return redirect(url_for("admin"))

# -------------------------
# RELATÓRIO EXCEL
# -------------------------
@app.route("/baixar-relatorio")
def baixar_relatorio():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Relatório"

    ws.append(["Nome", "Disciplinas", "Data", "Hora", "Presença"])

    for p in agendamentos:
        ws.append([
            p["nome"],
            ", ".join(p["disciplinas"]),
            p["data"],
            p["hora"],
            "Presente" if p["presente"] else "Falta"
        ])

    file = io.BytesIO()
    wb.save(file)
    file.seek(0)

    return send_file(
        file,
        as_attachment=True,
        download_name="relatorio_presencas.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# -------------------------
# SAIR
# -------------------------
@app.route("/logout")
def logout():
    return redirect(url_for("agendar"))

# -------------------------
# START
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
