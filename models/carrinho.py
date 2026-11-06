"""Classe Carrinho: guarda na sessão do navegador as plantas escolhidas."""
from models.item_pedido import ItemPedido


class Carrinho:
    def __init__(self, sessao):
        self._sessao = sessao
        self._itens = sessao.setdefault("carrinho", {})   # {"id_da_planta": quantidade}

    def _salvar(self):
        self._sessao.modified = True

    def adicionar(self, planta, quantidade=1):
        nova = self._itens.get(str(planta.id), 0) + int(quantidade)
        self.alterar(planta, nova)

    def alterar(self, planta, quantidade):
        quantidade = int(quantidade)
        if quantidade <= 0:
            return self.remover(planta.id)
        if quantidade > planta.estoque:
            raise ValueError(f"Só temos {planta.estoque} unidade(s) de {planta.nome}.")
        self._itens[str(planta.id)] = quantidade
        self._salvar()

    def remover(self, planta_id):
        self._itens.pop(str(planta_id), None)
        self._salvar()

    def esvaziar(self):
        self._itens.clear()
        self._salvar()

    def quantidade_total(self):
        return sum(self._itens.values())

    def itens(self, repo_plantas):
        """Monta a lista de ItemPedido consultando os dados atuais no banco."""
        lista = []
        for pid, qtd in list(self._itens.items()):
            p = repo_plantas.buscar(int(pid))
            if p is None or not p.disponivel():
                self.remover(pid)              # planta sumiu ou acabou o estoque
                continue
            lista.append(ItemPedido(p.id, p.nome, p.preco, min(qtd, p.estoque), p.imagem))
        return lista
