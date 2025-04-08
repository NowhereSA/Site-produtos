from flask import Flask, render_template, url_for, redirect, request, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['produtos']
collection = db['produtos']

def carregar_produtos():
    try:
        with open("produtos.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

@app.route("/produtos", methods=["GET"])
def home():
    documentos = list(collection.find({}, {"_id": 0}))
    return render_template('home.html', dados=documentos)

@app.route("/produtos/json", methods=["GET"])
def produtos_json():
    produtos = carregar_produtos()
    return jsonify(produtos)

@app.route("/produtos/adicionar", methods=["POST", "GET"])
def adicionar():
    nome = request.form.get("nome")
    id = request.form.get("id")
    preco = request.form.get("preco")
    if nome and id and preco:
        documentos = list(collection.find({}, {"_id": 0}))
        id_existente = any(d["id"] == int(id) for d in documentos)
        if id_existente:
            return redirect(url_for('adicionar'))
        else:   
            db.produtos.insert_one({"id": int(id), "nome": nome, "preco": float(preco)})
            return render_template("produtosAdicionar.html", mensagem="Produto adicionado com sucesso!")
    return render_template("produtosAdicionar.html", mensagem="Preencha todos os campos!")

@app.route("/", methods=["GET"])
def redirecionar():
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
    
