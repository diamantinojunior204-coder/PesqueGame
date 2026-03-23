from flask import Flask, render_template_string, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "fishbet_secret"

# =========================
# CONFIG
# =========================
CUSTO_PESCARIA = 5

peixes = [
    {"nome": "Tilápia", "valor": 2, "chance": 40, "img": "/static/peixes/tilapia.jpg"},
    {"nome": "Lambari", "valor": 4, "chance": 30, "img": "/static/peixes/lambari.jpg"},
    {"nome": "Baiacu", "valor": 6, "chance": 20, "img": "/static/peixes/baiacu.jpg"},
    {"nome": "Dourado", "valor": 10, "chance": 9, "img": "/static/peixes/dourado.jpg"},
    {"nome": "Tubarão", "valor": 50, "chance": 1, "img": "/static/peixes/tubarao.jpg"},
]

# =========================
# FUNÇÃO DE SORTEIO
# =========================
def sortear_peixe():
    sorte = random.randint(1, 100)
    acumulado = 0

    for peixe in peixes:
        acumulado += peixe["chance"]
        if sorte <= acumulado:
            return peixe

# =========================
# ROTAS
# =========================
@app.route("/")
def index():
    if "saldo" not in session:
        session["saldo"] = 100  # saldo inicial

    return render_template_string(html)

@app.route("/api/pescar")
def pescar():
    saldo = session.get("saldo", 0)

    if saldo < CUSTO_PESCARIA:
        return jsonify({"erro": "Saldo insuficiente!"})

    peixe = sortear_peixe()

    # desconta aposta
    saldo -= CUSTO_PESCARIA

    # soma prêmio
    saldo += peixe["valor"]

    session["saldo"] = saldo

    return jsonify({
        "nome": peixe["nome"],
        "valor": peixe["valor"],
        "img": peixe["img"],
        "saldo": saldo
    })

# =========================
# HTML + CSS + JS
# =========================
html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>🎣 FishBet</title>

<style>
body{
    margin:0;
    font-family: Arial;
    background: linear-gradient(#4facfe, #00f2fe);
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    color:white;
}

.game{
    text-align:center;
    background: rgba(0,0,0,0.4);
    padding:30px;
    border-radius:20px;
    box-shadow:0 0 20px rgba(0,0,0,0.5);
}

button{
    padding:15px 30px;
    font-size:18px;
    border:none;
    border-radius:10px;
    background: gold;
    cursor:pointer;
    font-weight:bold;
}

button:hover{
    transform: scale(1.1);
}

img{
    width:120px;
    margin:20px;
}

#resultado{
    margin-top:10px;
    font-size:18px;
}
</style>

</head>
<body>

<div class="game">
    <h1>🎣 FishBet</h1>
    <h3>Saldo: R$ <span id="saldo">100</span></h3>

    <img id="peixe" src="">

    <br>
    <button onclick="pescar()">PESCAR 🎣 (R$5)</button>

    <p id="resultado"></p>
</div>

<script>
function pescar(){
    const resultado = document.getElementById("resultado");
    const img = document.getElementById("peixe");

    resultado.innerText = "🎣 Lançando linha...";
    img.src = "";

    setTimeout(() => {
        fetch("/api/pescar")
        .then(r => r.json())
        .then(data => {

            if(data.erro){
                resultado.innerText = data.erro;
                return;
            }

            img.src = data.img;

            resultado.innerText =
                "Você pescou: " + data.nome +
                " 🐟 e ganhou R$" + data.valor;

            document.getElementById("saldo").innerText = data.saldo;
        });

    }, 2000);
}
</script>

</body>
</html>
"""

# =========================
app.run(debug=True)
