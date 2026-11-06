"""PedidoRepository: operações SQL de pedidos e itens_pedido."""
from database.conexao import conectar
from models.pedido import Pedido, STATUS
from models.item_pedido import ItemPedido
from models.usuario import Usuario

SQL_PEDIDO = """SELECT p.id, p.data, p.status, p.usuario_id,
                       u.nome AS u_nome, u.email AS u_email, u.tipo AS u_tipo
                FROM pedidos p JOIN usuarios u ON u.id = p.usuario_id"""


class PedidoRepository:
    def _montar(self, con, r):
        """Transforma a linha do banco em um objeto Pedido completo."""
        usuario = Usuario(r["u_nome"], r["u_email"], r["u_tipo"], id=r["usuario_id"])
        itens = [ItemPedido(i["planta_id"], i["nome"], i["preco_unitario"], i["quantidade"], id=i["id"])
                 for i in con.execute("""SELECT i.*, pl.nome FROM itens_pedido i
                                         JOIN plantas pl ON pl.id = i.planta_id
                                         WHERE i.pedido_id = ?""", (r["id"],))]
        return Pedido(usuario, itens, r["status"], r["data"], r["id"])

    def salvar(self, pedido):
        """Grava pedido + itens e baixa o estoque. Se algo falhar, nada é gravado."""
        pedido.validar()
        with conectar() as con:
            for it in pedido.itens:
                r = con.execute("UPDATE plantas SET estoque = estoque - ? WHERE id = ? AND estoque >= ?",
                                (it.quantidade, it.planta_id, it.quantidade))
                if r.rowcount == 0:
                    raise ValueError(f"Estoque insuficiente de {it.nome}.")
            pedido.id = con.execute("INSERT INTO pedidos (usuario_id, total, status) VALUES (?, ?, ?)",
                                    (pedido.usuario.id, pedido.total, pedido.status)).lastrowid
            con.executemany("""INSERT INTO itens_pedido (pedido_id, planta_id, quantidade, preco_unitario)
                               VALUES (?, ?, ?, ?)""",
                            [(pedido.id, i.planta_id, i.quantidade, i.preco_unitario) for i in pedido.itens])
        return pedido.id

    def listar(self):
        with conectar() as con:
            return [self._montar(con, r) for r in con.execute(SQL_PEDIDO + " ORDER BY p.id DESC")]

    def buscar(self, id):
        with conectar() as con:
            r = con.execute(SQL_PEDIDO + " WHERE p.id = ?", (id,)).fetchone()
            return self._montar(con, r) if r else None

    def atualizar_status(self, id, status):
        if status not in STATUS:
            raise ValueError("Status inválido.")
        with conectar() as con:
            con.execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, id))

    def excluir(self, id):
        with conectar() as con:       # os itens são apagados junto (ON DELETE CASCADE)
            con.execute("DELETE FROM pedidos WHERE id = ?", (id,))
