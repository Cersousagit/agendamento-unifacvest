from flask import Flask, render_template, request, redirect
import itertools

app = Flask(__name__)
agendamentos=[]
ids=itertools.count(1)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def auth():
    u=request.form["usuario"]
    s=request.form["senha"]
    if u=="admin" and s=="admin123":
        return redirect("/admin")
    if u=="aluno" and s=="aluno123":
        return redirect("/agendar")
    return redirect("/")

@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    msg = None

    if request.method == "POST":
        agendamentos.append({
            "id": next(contador_id),
            "nome": request.form["nome"],
            "disciplinas": request.form["disciplinas"],
            "data": request.form["data"],
            "hora": request.form["hora"],
            "presente": False
        })
        msg = "Agendamento realizado com sucesso!"

    return render_template("agendar.html", msg=msg)


@app.route("/admin")
def admin():
    return render_template("admin.html", agendamentos=agendamentos)

@app.route("/presenca/<int:id>")
def presenca(id):
    for a in agendamentos:
        if a["id"]==id:
            a["presente"]=True
    return redirect("/admin")

@app.route("/logout")
def logout():
    return redirect("/")

if __name__=="__main__":
    app.run()
