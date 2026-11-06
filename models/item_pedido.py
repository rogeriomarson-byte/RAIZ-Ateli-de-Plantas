"""Classe ItemPedido: uma planta (com quantidade) dentro de um pedido ou do carrinho."""


class ItemPedido:
    def __init__(self, planta_id, nome, preco_unitario, quantidade, imagem=None, id=None):
        self.id = id
        self.planta_id = planta_id
        self.nome = nome
        self.preco_unitario = float(preco_unitario)
        self.quantidade = int(quantidade)
        self.imagem = imagem

    @property
    def subtotal(self):
        return round(self.preco_unitario * self.quantidade, 2)
