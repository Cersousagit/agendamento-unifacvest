from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "unifacvest_secreta"

DB_NAME = "database.db"


# ---------------- BANCO ----------------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            disciplina TEXT,
            data TEXT,
            hora TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["usuario"]
        senha = request.form["senha"]

        if user == "aluno" and senha == "aluno123":
            session["perfil"] = "aluno"
            return redirect(url_for("agendar"))

        if user == "admin" and senha == "admin123":
            session["perfil"] = "admin"
            return redirect(url_for("admin"))

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")


# ---------------- AGENDAMENTO ----------------
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if session.get("perfil") != "aluno":
        return redirect(url_for("login"))

    if request.method == "POST":
        nome = request.form["nome"]
        disciplinas = request.form.getlist("disciplinas[]")
        data = request.form["data"]
        hora = request.form["hora"]

        conn = get_db()
        for d in disciplinas:
            conn.execute(
                "INSERT INTO agendamentos (nome, disciplina, data, hora, status) VALUES (?, ?, ?, ?, ?)",
                (nome, d, data, hora, "pendente")
            )
        conn.commit()
        conn.close()

        return render_template("agendar.html", sucesso=True)

    return render_template("agendar.html")


# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    if session.get("perfil") != "admin":
        return redirect(url_for("login"))

    conn = get_db()
    provas = conn.execute("""
        SELECT * FROM agendamentos
        WHERE status='pendente'
        ORDER BY data, hora
    """).fetchall()

    total_pendentes = len(provas)
    total_confirmadas = conn.execute(
        "SELECT COUNT(*) FROM agendamentos WHERE status='confirmado'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        provas=provas,
        pendentes=total_pendentes,
        confirmadas=total_confirmadas
    )


# ---------------- CONFIRMAR ----------------
@app.route("/confirmar/<int:id>")
def confirmar(id):
    if session.get("perfil") != "admin":
        return redirect(url_for("login"))

    conn = get_db()
    conn.execute(
        "UPDATE agendamentos SET status='confirmado' WHERE id=?",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


# ---------------- SAIR ----------------
@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
