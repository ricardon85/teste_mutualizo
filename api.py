#-*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from classes import *

app = Flask(__name__)

produtos = []
carrinho = Carrinho()
pedidos = []

@app.route('/produtos', methods=['GET'])
def lista_produtos():
    produtos_json = []
    for id, produto in enumerate(produtos):
        produtos_json.append({
            "nome": produto.nome,
            "preco": produto.preco,
            "estoque": produto.estoque
        })
    return jsonify(produtos_json), 200

@app.route('/produto/<int:id>', methods=['GET'])
def lista_produto(id):
    produtos_json = []
    produtos_json.append({
        "nome": produtos[id].nome,
        "preco": produtos[id].preco,
        "estoque": produtos[id].estoque
    })
    return jsonify(produtos_json), 200

@app.route('/carrinho', methods=['GET'])
def lista_itens():
    itens_json = []
    for item in carrinho.itens:
        itens_json.append({
            "produto": item['produto'].__dict__,
            "quantidade": item['quantidade']
        })
    return jsonify(itens_json), 200

@app.route('/pedidos', methods=['GET'])
def lista_pedidos():
    pedidos_json = []
    for id, pedido in enumerate(pedidos):
        produtos_json = []
        for produto in pedido.produtos:
            produtos_json.append({
                "produto": produto["produto"].__dict__,
                "quantidade": produto["quantidade"]
            })
        pedidos_json.append({
            "pedido "+str(id): produtos_json,
            "total": pedido.total
        })
    return jsonify(pedidos_json), 200

@app.route('/pedido/<int:id>', methods=['GET'])
def lista_pedido(id):
    pedido_json = []
    produtos_json = []
    for produto in pedidos[id].produtos:
        produtos_json.append({
            "produto": produto["produto"].__dict__,
            "quantidade": produto["quantidade"]
        })
    pedido_json.append({
        "pedido "+str(id): produtos_json,
        "total": pedidos[id].total
    })
    return jsonify(pedido_json), 200

@app.route('/adiciona_produto/<int:id>/<int:quantidade>', methods=['GET'])
def adiciona_produto(id, quantidade):
    if carrinho.adiciona_produto(produtos[id], quantidade):
        return jsonify({"mensagem": "Produto adicionado ao carrinho com sucesso."}), 200
    else:
        return jsonify({"mensagem": "Não foi possível adicionar o produto ao carrinho."}), 400

@app.route('/remove_produto/<int:id>/<int:quantidade>', methods=['GET'])
def remove_produto(id, quantidade):
    if carrinho.remove_produto(produtos[id], -quantidade):
        return jsonify({"mensagem": "Produto removido do carrinho com sucesso."}), 200
    else:
        return jsonify({"mensagem": "Não foi possível remover o produto do carrinho."}), 400

@app.route('/finaliza_compra', methods=['GET'])
def finaliza_compra():
    pedido = carrinho.finaliza()
    if pedido:
        pedidos.append(pedido)
        return jsonify({"mensagem": "Compra finalizada com sucesso.", "total": pedido.total}), 200
    else:
        return jsonify({"mensagem": "Não foi possível finalizar a compra."}), 400