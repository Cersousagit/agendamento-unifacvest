from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB = "dados.db"

def criar_banco():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            disciplinas TEXT,
            data TEXT,
            horario TEXT,
            presente INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

criar_banco()

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Agendamento de Provas UNIFACVEST</title>
<style>
body { font-family: Arial; background: white; color: #b30000; text-align: center; }
form { background: #f2f2f2; padding: 20px; width: 300px; margin: auto; border-radius: 10px; }
input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
button { background: #b30000; color: white; border: none; padding: 10px; }
</style>
</head>
<body>
<h2>Agendamento de Provas - UNIFACVEST</h2>
<form method="post">
<input name="nome" placeholder="Nome completo" required>
<textarea name="disciplinas" placeholder="Disciplinas (uma por linha)" required></textarea>
<input type="date" name="data" required>
<input type="time" name="horario" required>
<button type="submit">Enviar</button>
</form>
<p>{{msg}}</p>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    msg = ""
    if request.method == "POST":
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute(
            "INSERT INTO agendamentos (nome, disciplinas, data, horario) VALUES (?,?,?,?)",
            (request.form["nome"], request.form["disciplinas"], request.form["data"], request.form["horario"])
        )
        conn.commit()
        conn.close()
        msg = "Agendamento realizado com sucesso!"
    return render_template_string(HTML, msg=msg)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

