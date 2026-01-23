from flask import Flask, render_template, redirect, url_for
import itertools

app = Flask(__name__)

# Banco fake
agendamentos = []
contador_id = itertools.count(1)

# Registro inicial
agendamentos.append({
    "id": next(contador_id),
    "nome": "Marcos Aurelio",
    "disciplinas": "1,2,3",
    "data": "2026-02-05",
    "hora": "11:00",
    "presente": False
})

@app.route("/")
def index():
    return redirect(url_for("admin"))

@app.route("/admin")
def admin():
    total_presentes = sum(1 for a in agendamentos if a["presente"])

    datas = []
    quantidades = []

    for a in agendamentos:
        if a["data"] not in datas:
            datas.append(a["data"])
            quantidades.append(1)
        else:
            i = datas.index(a["data"])
            quantidades[i] += 1

    return render_template(
        "admin.html",
        agendamentos=agendamentos,
        total_presentes=total_presentes,
        datas=datas,
        quantidades=quantidades
    )

@app.route("/presenca/<int:id>")
def presenca(id):
    for a in agendamentos:
        if a["id"] == id:
            a["presente"] = True
            break
    return redirect(url_for("admin"))

@app.route("/logout")
def logout():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
