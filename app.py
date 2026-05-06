from flask import Flask, render_template, request, jsonify, session

# CRIA O FLASK PRIMEIRO
app = Flask(__name__)

app.secret_key = "secreto"


@app.route("/")
def inicio():
    return "Olá"


@app.route("/cofre")
def cofre():
    return render_template("index.html")


@app.route("/process_attempt", methods=["POST"])
def process_attempt():

    if "user_id" not in session:
        return jsonify({
            "message":"Você precisa estar logado."
        })

    action = request.form.get("action")

    if action == "try_open":

        return jsonify({
            "message":"Pague R$1,00 no PIX.",
            "pix_key":"pix@diamante.com"
        })

    return jsonify({
        "message":"Ação inválida"
    })


if __name__ == "__main__":
    app.run(debug=True)
