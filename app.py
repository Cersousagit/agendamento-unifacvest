from flask import Flask, render_template, request, redirect, session, url_for, send_file
import json
import os
from datetime import datetime
from openpyxl import Workbook

app = Flask(__name__)
app.secret_key = "unifacvest-secret"

DATA_FILE = 'agendamentos.json'

def load_agendamentos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_agendamentos(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

agendamentos = load_agendamentos()
contador_id = max([a.get('id', 0) for a in agendamentos], default=0) + 1

def remover_expirados():
    global agendamentos
    agora = datetime.now()
    agendamentos[:] = [a for a in agendamentos if not (
        a.get('status') == 'confirmada' and
        datetime.strptime(f"{a['data']} {a['hora']}", "%Y-%m-%d %H:%M") < agora
    )]
    save_agendamentos(agendamentos)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        if usuario == "admin" and senha == "admin123":
            session["usuario"] = "admin"
            return redirect("/admin")
        if usuario == "aluno" and senha == "aluno123":
            session["usuario"] = "aluno"
            return redirect("/agendar")
        return render_template("login.html", erro="Usuário ou senha inválidos")
    return render_template("login.html")

@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    global contador_id, agendamentos
    if session.get("usuario") != "aluno":
        return redirect("/")
    if request.method == "POST":
        try:
            disciplinas = request.form.getlist("disciplinas")  # Lista de disciplinas
            if not disciplinas:
                return render_template("agendar.html", erro="Adicione pelo menos uma disciplina")
            novo = {
                "id": contador_id,
                "nome": request.form["nome"],
                "disciplinas": disciplinas,
                "data": request.form["data"],
                "hora": request.form["hora"],
                "status": "pendente"
            }
            agendamentos.append(novo)
            save_agendamentos(agendamentos)
            contador_id += 1
            return render_template("agendar.html", sucesso=True)
        except KeyError:
            return render_template("agendar.html", erro="Dados inválidos")
    return render_template("agendar.html")

# ... (código anterior permanece)

@app.route("/admin")
def admin():
    if session.get("usuario") != "admin":
        return redirect("/")
    remover_expirados()
    filter_start = request.args.get("filter_start")
    filter_end = request.args.get("filter_end")
    pendentes = sorted([a for a in agendamentos if a["status"] == "pendente"], key=lambda x: (x["data"], x["hora"]))
    confirmadas = sorted([a for a in agendamentos if a["status"] == "confirmada"], key=lambda x: (x["data"], x["hora"]))
    if filter_start and filter_end:
        pendentes = [p for p in pendentes if filter_start <= p["data"] <= filter_end]
        confirmadas = [c for c in confirmadas if filter_start <= c["data"] <= filter_end]
    return render_template("admin.html", pendentes=pendentes, confirmadas=confirmadas)

@app.route("/confirmar/<int:id>")
def confirmar(id):
    if session.get("usuario") != "admin":
        return redirect("/")
    for a in agendamentos:
        if a["id"] == id:
            a["status"] = "confirmada"
            save_agendamentos(agendamentos)
            break
    return redirect("/admin")

@app.route("/presenca/<int:id>")
def presenca(id):
    if session.get("usuario") != "admin":
        return redirect("/")
    global agendamentos
    agendamentos = [a for a in agendamentos if a["id"] != id]  # Remove ao confirmar presença
    save_agendamentos(agendamentos)
    return redirect("/admin")

@app.route("/download")
def download():
    if session.get("usuario") != "admin":
        return redirect("/")
    start = request.args.get("start")
    end = request.args.get("end")
    if not start or not end:
        return redirect("/admin")
    wb = Workbook()
    ws = wb.active
    ws.append(["ID", "Nome", "Disciplinas", "Data", "Hora", "Status"])
    for a in agendamentos:
        if start <= a["data"] <= end:
            ws.append([a["id"], a["nome"], ", ".join(a["disciplinas"]), a["data"], a["hora"], a["status"]])
    filename = f"agendamentos_{start}_to_{end}.xlsx"
    wb.save(filename)
    return send_file(filename, as_attachment=True)

@app.route("/sair")
def sair():
    session.clear()
    return redirect("/")

@app.route("/healthz")
def healthz():
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
