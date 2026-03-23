from flask import Flask, render_template_string, jsonify, session
import random



app = Flask(__name__, static_folder="static")
app.secret_key = "fishbet_secret"
CUSTO = 5
peixes = [
    {"nome": "Tilápia", "valor": 2, "chance": 40, "img": "static/peixes/tilapia.jpg"},
    {"nome": "Lambari", "valor": 4, "chance": 30, "img": "static/peixes/lambari.jpg"},
    {"nome": "Baiacu", "valor": 6, "chance": 20, "img": "static/peixes/baiacu.jpg"},
    {"nome": "Dourado", "valor": 10, "chance": 9, "img": "static/peixes/dourado.jpg"},
    {"nome": "Tubarão", "valor": 50, "chance": 1, "img": "static/peixes/tubarao.jpg"},
]


def sortear():
    s = random.randint(1,100)
    acum = 0
    for p in peixes:
        acum += p["chance"]
        if s <= acum:
            return p

@app.route("/")
def index():
    if "saldo" not in session:
        session["saldo"] = 100
    return render_template_string(html)

@app.route("/api/pescar")
def pescar():
    saldo = session.get("saldo",0)

    if saldo < CUSTO:
        return jsonify({"erro":"Sem saldo!"})

    peixe = sortear()

    saldo -= CUSTO
    saldo += peixe["valor"]

    session["saldo"] = saldo

    return jsonify({
        "nome": peixe["nome"],
        "valor": peixe["valor"],
        "img": peixe["img"],
        "saldo": saldo
    })

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>FishBet</title>

<style>
body{
margin:0;
font-family:Arial;
background:linear-gradient(#4facfe,#00f2fe);
display:flex;
justify-content:center;
align-items:center;
height:100vh;
color:white;
}

.game{
text-align:center;
background:rgba(0,0,0,0.4);
padding:25px;
border-radius:20px;
}

.lago{
width:250px;
height:150px;
background:radial-gradient(circle,#00c6ff,#0072ff);
border-radius:50%;
margin:20px auto;
position:relative;
overflow:hidden;
}

.lago::after{
content:"";
position:absolute;
width:200%;
height:200%;
top:-50%;
left:-50%;
background:repeating-radial-gradient(circle,rgba(255,255,255,0.2)0px,rgba(255,255,255,0.2)2px,transparent 3px,transparent 20px);
animation:agua 3s linear infinite;
}

@keyframes agua{
from{transform:rotate(0deg);}
to{transform:rotate(360deg);}
}

#linha{
width:2px;
height:0;
background:white;
position:absolute;
top:0;
left:50%;
transition:0.5s;
}

#peixe{
width:120px;
opacity:0;
transform:scale(0.5);
transition:0.5s;
margin-top:10px;
}

.show{
opacity:1;
transform:scale(1.2);
}

button{
padding:15px 25px;
font-size:18px;
border:none;
border-radius:10px;
background:gold;
cursor:pointer;
}

</style>
</head>

<body>

<div class="game">
<h1>🎣 FishBet</h1>
<h3>Saldo: R$ <span id="saldo">100</span></h3>

<div class="lago">
<div id="linha"></div>
</div>

<img id="peixe">

<br><br>
<button onclick="pescar()">PESCAR 🎣 (R$5)</button>

<p id="resultado"></p>
</div>

<script>
function pescar(){
let res = document.getElementById("resultado");
let img = document.getElementById("peixe");
let linha = document.getElementById("linha");

res.innerText = "🎣 Jogando linha...";
img.classList.remove("show");
img.src = "";

linha.style.height = "120px";

setTimeout(()=>{
res.innerText = "💧 Algo puxou...";
},1000);

setTimeout(()=>{
fetch("/api/pescar")
.then(r=>r.json())
.then(d=>{

if(d.erro){
res.innerText = d.erro;
linha.style.height="0";
return;
}

linha.style.height="0";

img.src = d.img;
img.classList.add("show");

res.innerText = "🐟 "+d.nome+" - R$"+d.valor;
document.getElementById("saldo").innerText = d.saldo;

});
},2000);
}
</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run()
