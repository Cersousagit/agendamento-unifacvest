from flask import Flask, render_template, request, redirect, url_for, send_file
from datetime import datetime, date
from openpyxl import Workbook
import io

app = Flask(__name__)

agendamentos = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/agendar")
    return render_template("login.html")


@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    msg = None
    if request.method == "POST":
        nome = request.form.get("nome")
        disciplinas = request.form.getlist("disciplinas[]")
        data = request.form.get("data")
        hora = request.form.get("hora")

        if not nome or not disciplinas:
            return "Bad Request", 400

        agendamentos.append({
            "nome": nome,
            "disciplinas": disciplinas,
            "data": data,
            "hora": hora,
            "presente": None
        })

        msg = "Agendamento realizado com sucesso"

    return render_template("agendar.html", msg=msg)


@app.route("/admin")
def admin():
    hoje = date.today()

    ativos = [
        a for a in agendamentos
        if datetime.strptime(a["data"], "%Y-%m-%d").date() >= hoje
    ]

    ativos.sort(key=lambda x: (x["data"], x["hora"]))

    presencas = sum(1 for a in ativos if a["presente"] is True)
    faltas = sum(1 for a in ativos if a["presente"] is False)

    return render_template(
        "admin.html",
        agendamentos=ativos,
        presencas=presencas,
        faltas=faltas
    )


@app.route("/presenca/<int:i>")
def presenca(i):
    agendamentos[i]["presente"] = True
    return redirect("/admin")


@app.route("/falta/<int:i>")
def falta(i):
    agendamentos[i]["presente"] = False
    return redirect("/admin")


@app.route("/relatorio")
def relatorio():
    wb = Workbook()
    ws = wb.active
    ws.append(["Nome", "Disciplinas", "Data", "Hora", "Status"])

    for a in agendamentos:
        status = "Presente" if a["presente"] else "Falta"
        ws.append([
            a["nome"],
            ", ".join(a["disciplinas"]),
            a["data"],
            a["hora"],
            status
        ])

    file = io.BytesIO()
    wb.save(file)
    file.seek(0)

    return send_file(
        file,
        download_name="relatorio_presenca.xlsx",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
