@app.route("/process_attempt", methods=["POST"])
def process_attempt():
    
    if "user_id" not in session:
        return jsonify({"message": "Você precisa estar logado."})

    user_id = session["user_id"]

    conn = conectar()
    c = conn.cursor()

    # pegar saldo
    c.execute("SELECT saldo FROM usuarios WHERE id=%s", (user_id,))
    saldo = c.fetchone()[0]

    if saldo >= 1:
        # descontar
        novo_saldo = saldo - 1
        c.execute("UPDATE usuarios SET saldo=%s WHERE id=%s", (novo_saldo, user_id))
        conn.commit()

        import random
        ganhou = random.choice([True, False])

        if ganhou:
            return jsonify({"message": "🎉 Você abriu o cofre!"})
        else:
            return jsonify({"message": "❌ Não foi dessa vez!"})
    else:
        return jsonify({"message": "Saldo insuficiente."})
