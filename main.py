#-*- coding: utf-8 -*-

## Questão 1 ##
def fibonacci(x):
    lista = []
    for i in range(0, x+1):
        if len(lista) < 2:
            lista.append(i)
        else:
            lista.append(lista[i-2]+lista[i-1])
    return lista[len(lista)-1]

def fibonacci2(x):
    a_soma, soma = 0, 1
    for i in range(0, x-1):
        a_soma, soma = soma, a_soma + soma
    return soma

## Questão 2 ##
from api import *

## Teste ##
if __name__ == '__main__':
    print("Fibonacci 1:")
    print(fibonacci(6))
    print("Fibonacci 2:")
    print(fibonacci2(6))

    produtos.append(Produto("Produto 1", 1.10, 10))
    produtos.append(Produto("Produto 2", 2.20, 20))
    produtos.append(Produto("Produto 3", 3.30, 30))
    produtos.append(Produto("Produto 4", 4.40, 40))
    produtos.append(Produto("Produto 5", 5.50, 50))

    carrinho.adiciona_produto(produtos[0])
    carrinho.adiciona_produto(produtos[1], 2)
    carrinho.adiciona_produto(produtos[2], 3)
    carrinho.remove_produto(produtos[2], 1)

    pedidos.append(carrinho.finaliza())

    carrinho.adiciona_produto(produtos[3])
    carrinho.adiciona_produto(produtos[4], 2)

    app.run(debug=True)