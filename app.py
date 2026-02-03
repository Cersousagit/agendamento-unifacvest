# ... (código anterior permanece igual, exceto na rota /admin)

@app.route("/admin")
def admin():
    if session.get("usuario") != "admin":
        return redirect("/")
    limpar_historico_antigo()
    remover_expirados()
    pendentes = sorted([a for a in agendamentos if a["status"] == "pendente"], key=lambda x: (x["data"], x["hora"]))
    confirmadas = sorted([a for a in agendamentos if a["status"] == "confirmada"], key=lambda x: (x["data"], x["hora"]))
    if filter_start and filter_end:
        pendentes = [p for p in pendentes + [h for h in historico if h["status"] == "pendente"] if filter_start <= p["data"] <= filter_end]
        confirmadas = [c for c in confirmadas + [h for h in historico if h["status"] == "confirmada"] if filter_start <= c["data"] <= filter_end]
    
    # Dados para gráficos
    total_pendentes = len(pendentes)
    total_confirmadas = len(confirmadas)
    # Simulação de provas por mês (últimos 6 meses; ajuste para dados reais se necessário)
    from collections import defaultdict
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

# ... (restante do código permanece igual)
