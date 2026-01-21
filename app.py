@app.route("/presente/<int:index>")
def marcar_presenca(index):
    if session.get("perfil") != "admin":
        return redirect("/")

    global agendamentos

    if index < len(agendamentos):
        agendamentos[index]["presente"] = True

    return redirect("/admin")
