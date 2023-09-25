#-*- coding: utf-8 -*-

class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def possui_estoque(self, quantidade):
        return self.estoque >= quantidade

    def ajusta_estoque(self, quantidade):
        if self.estoque + quantidade >= 0:
            self.estoque += quantidade
            return True
        else:
            return False

class Carrinho:
    def __init__(self):
        self.itens = []

    def gerencia_quantidade_item_carrinho(self, produto, quantidade):
        for i in self.itens:
            if i["produto"] == produto:
                if i["quantidade"] + quantidade >= 0:
                    i["quantidade"] += quantidade
                    return i
        return None

    def adiciona_produto(self, produto, quantidade=1):
        if produto.possui_estoque(quantidade):
            item = self.gerencia_quantidade_item_carrinho(produto, quantidade)
            if not item:
                item_carrinho = {"produto": produto, "quantidade": quantidade}
                self.itens.append(item_carrinho)
            return True
        else:
            return False

    def remove_produto(self, produto, quantidade=1):
        item = self.gerencia_quantidade_item_carrinho(produto, quantidade)
        if item:
            if item["quantidade"] == 0:
                self.itens.remove(item)
            return True
        return False

    def totaliza(self):
        return sum(i["produto"].preco * i["quantidade"] for i in self.itens)

    def finaliza(self):
        for i in self.itens:
            if i["produto"].possui_estoque(i["quantidade"]):
                if not i["produto"].ajusta_estoque(i["quantidade"]):
                    return None
        pedido = Pedido(self.itens, self.totaliza())
        self.itens = []
        return pedido

class Pedido:
    def __init__(self, produtos, total):
        self.produtos = produtos
        self.total = total