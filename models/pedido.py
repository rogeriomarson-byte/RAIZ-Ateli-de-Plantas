"""Classe Pedido: pertence a um Usuario e contém vários ItemPedido."""
STATUS = ("Recebido", "Em preparo", "Enviado", "Entregue", "Cancelado")


class Pedido:
    def __init__(self, usuario, itens=None, status="Recebido", data=None, id=None):
        self.id = id
        self.usuario = usuario              # relacionamento: pedido -> usuário
        self.itens = itens or []            # relacionamento: pedido -> itens
        self.status = status
        self.data = data

    def adicionar_item(self, item):
        self.itens.append(item)

    @property
    def total(self):
        return round(sum(i.subtotal for i in self.itens), 2)

    def validar(self):
        if not self.itens:
            raise ValueError("O pedido precisa ter pelo menos um item.")
        if self.status not in STATUS:
            raise ValueError("Status de pedido inválido.")
