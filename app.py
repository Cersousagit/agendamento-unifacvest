from flask import Flask, render_template, request, redirect, session, url_for, send_file
import json
import os
from datetime import datetime, timedelta
from openpyxl import Workbook
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "unifacvest-secret"

DATA_FILE = 'agendamentos.json'
HISTORICO_FILE = 'historico.json'

def load_agendamentos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_agendamentos(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def load_historico():
    if os.path.exists(HISTORICO_FILE):
        with open(HISTORICO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_historico(data):
    with open(HISTORICO_FILE, 'w') as f:
        json.dump(data, f)

agendamentos = load_agendamentos()
historico = load_historico()
contador_id = max([a.get('id', 0) for a in agendamentos + historico], default=0) + 1

def limpar_historico_antigo():
    global historico
    agora = datetime.now()
    limite = agora - timedelta(days=365)  # Manter por 1 ano
    historico[:] = [h for h in historico if datetime.strptime(h['data'], "%Y-%m-%d") > limite]
    save_historico(historico)

def remover_expirados():
    global agendamentos, historico
    agora = datetime.now()
    expirados = [a for a in agendamentos if a.get('status') == 'confirmada' and datetime.strptime(f"{a['data']} {a['hora']}", "%Y-%m-%d %H:%M") < agora]
    for exp in expirados:
        historico.append(exp)
    agendamentos[:] = [a for a in agendamentos if a not in expirados]
    save_agendamentos(agendamentos)
    save_historico(historico)

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
            nome = request.form.get("nome", "").strip()
            data = request.form.get("data", "").strip()
            hora = request.form.get("hora", "").strip()
            disciplinas_raw = request.form.getlist("disciplinas")
            if not disciplinas_raw:
                disciplinas_raw = [request.form.get("disciplinas", "")]  # Fallback se não for lista
            disciplinas = [d.strip() for d in disciplinas_raw if d.strip()]
            
            if not nome or not data or not hora or not disciplinas:
                return render_template("agendar.html", erro="Todos os campos são obrigatórios")
            
            novo = {
                "id": contador_id,
                "nome": nome,
                "disciplinas": disciplinas,
                "data": data,
                "hora": hora,
                "status": "pendente"
            }
            agendamentos.append(novo)
            save_agendamentos(agendamentos)
            contador_id += 1
            return render_template("agendar.html", sucesso=True)
        except Exception as e:
            return render_template("agendar.html", erro="Erro interno. Tente novamente.")
    return render_template("agendar.html")



@app.route("/admin")
def admin():
    if session.get("usuario") != "admin":
        return redirect("/")
    limpar_historico_antigo()
    remover_expirados()
    filter_start = request.args.get("filter_start")
    filter_end = request.args.get("filter_end")
    pendentes = sorted([a for a in agendamentos if a["status"] == "pendente"], key=lambda x: (x["data"], x["hora"]))
    confirmadas = sorted([a for a in agendamentos if a["status"] == "confirmada"], key=lambda x: (x["data"], x["hora"]))
    if filter_start and filter_end:
        pendentes = [p for p in pendentes + [h for h in historico if h["status"] == "pendente"] if filter_start <= p["data"] <= filter_end]
        confirmadas = [c for c in confirmadas + [h for h in historico if h["status"] == "confirmada"] if filter_start <= c["data"] <= filter_end]
    
    # Dados para gráficos
    total_pendentes = len(pendentes)
    total_confirmadas = len(confirmadas)
    # Provas por mês (últimos 6 meses)
    provas_por_mes = defaultdict(int)
    for a in agendamentos + historico:
        mes = a["data"][:7]  # YYYY-MM
        provas_por_mes[mes] += 1
    meses = list(provas_por_mes.keys())[-6:]  # Últimos 6 meses
    valores_meses = [provas_por_mes[m] for m in meses]
    
    return render_template("admin.html", 
                           pendentes=pendentes, 
                           confirmadas=confirmadas,
                           total_pendentes=total_pendentes,
                           total_confirmadas=total_confirmadas,
                           meses=meses,
                           valores_meses=valores_meses)

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
    global agendamentos, historico
    item_removido = None
    for a in agendamentos:
        if a["id"] == id:
            item_removido = a
            break
    if item_removido:
        agendamentos.remove(item_removido)
        historico.append(item_removido)
        save_agendamentos(agendamentos)
        save_historico(historico)
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
    todos = agendamentos + historico
    for a in todos:
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
