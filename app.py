from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

simbolos = ["tigre.png", "moeda.png", "barra.png"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/spin")
def spin():
    resultado = [random.choice(simbolos) for _ in range(3)]

    # regra simples de ganho
    if resultado[0] == resultado[1] == resultado[2]:
        ganho = random.randint(50, 200)
    else:
        ganho = 0

    return jsonify({
        "resultado": resultado,
        "ganho": ganho
    })

if __name__ == "__main__":
    app.run()
