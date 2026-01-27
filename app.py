<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Agendamento de Provas</title>

<style>
body { font-family:Arial; background:#f4f6f8; }

header {
    background:#003366;
    color:white;
    padding:15px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

header img { height:45px; }

a.sair {
    color:white;
    text-decoration:none;
    background:#c62828;
    padding:8px 12px;
    border-radius:5px;
}

.card {
    background:white;
    width:420px;
    margin:30px auto;
    padding:20px;
    border-radius:8px;
}

input, button {
    width:100%;
    padding:10px;
    margin-top:8px;
}

button {
    background:#003366;
    color:white;
    border:none;
    cursor:pointer;
}

.plus {
    background:#2e7d32;
    margin-top:5px;
}

.instrucao {
    background:#e3f2fd;
    padding:10px;
    border-left:4px solid #1565c0;
    font-size:14px;
    margin-bottom:15px;
}

.sucesso {
    margin-top:10px;
    color:green;
    font-weight:bold;
    text-align:center;
}
</style>
</head>

<body>

<header>
<img src="{{ url_for('static', filename='unifacvest.png') }}">
<a href="/logout" class="sair">Sair</a>
</header>

<div class="card">

<h3>Agendamento de Provas</h3>

<div class="instrucao">
📌 <strong>Instruções:</strong><br>
• Preencha seu nome corretamente.<br>
• Adicione todas as disciplinas que deseja agendar.<br>
• Clique em <strong>+ Adicionar disciplina</strong> para incluir mais provas.<br>
• Confira a data e horário antes de enviar.
</div>

<form method="POST">

<input type="text" name="nome" placeholder="Nome do aluno" required>

<!-- DISCIPLINAS DINÂMICAS -->
<div id="disciplinas">
    <input type="text" name="disciplinas" placeholder="Disciplina 1" required>
</div>

<button type="button" class="plus" onclick="adicionarDisciplina()">+ Adicionar disciplina</button>

<input type="date" name="data" required>
<input type="time" name="hora" required>

<button type="submit">Enviar</button>

{% if msg %}
<div class="sucesso">✅ {{ msg }}</div>
{% endif %}

</form>
</div>

<script>
function adicionarDisciplina() {
    const div = document.getElementById("disciplinas");
    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Outra disciplina";
    input.onchange = atualizarDisciplinas;
    div.appendChild(input);
}

function atualizarDisciplinas() {
    const inputs = document.querySelectorAll("#disciplinas input");
    let valores = [];
    inputs.forEach(i => {
        if (i.value.trim() !== "") {
            valores.push(i.value.trim());
        }
    });
    inputs[0].name = "disciplinas";
    inputs[0].value = valores.join(" | ");
}
</script>

</body>
</html>
