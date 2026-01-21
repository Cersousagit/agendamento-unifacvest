from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "unifacvest123"

DB_NAME = "database.db"

# ---------------- BANCO ----------------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def criar_banco():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            disciplinas TEXT,
            data TEXT,
            hora TEXT,
            presente INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

criar_banco()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "admin" and senha == "Admin123":
            session["perfil"] = "admin"
            return redirect("/admin")

        elif senha == "Aluno123":
            session["perfil"] = "aluno"
            return redirect("/agendar")

        else:
            erro = "Usuário ou senha inválidos"

    return render_template("login.html", erro=erro)

# ---------------- AGENDAR ----------------
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if session.get("perfil") != "aluno":
        return redirect("/")

    msg = ""
    if request.method == "POST":
        conn = get_db()
        conn.execute("""
            INSERT INTO agendamentos (nome, disciplinas, data, hora)
            VALUES (?, ?, ?, ?)
        """, (
            request.form["nome"],
            request.form["disciplinas"],
            request.form["data"],
            request.form["hora"]
        ))
        conn.commit()
        conn.close()
        msg = "Agendamento realizado com sucesso!"

    return render_template("agendar.html", msg=msg)

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    if session.get("perfil") != "admin":
        return redirect("/")

    hoje = datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    agendamentos = conn.execute("""
        SELECT * FROM agendamentos
        WHERE data >= ?
        ORDER BY data, hora
    """, (hoje,)).fetchall()
    conn.close()

    return render_template("admin.html", agendamentos=agendamentos)

# ---------------- PRESENÇA ----------------
@app.route("/presenca/<int:id>")
def presenca(id):
    if session.get("perfil") != "admin":
        return redirect("/")

    conn = get_db()
    conn.execute("UPDATE agendamentos SET presente = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- START ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
