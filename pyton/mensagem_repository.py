"""MensagemRepository: operações SQL da tabela mensagens."""
from database.conexao import conectar
from models.mensagem import Mensagem


class MensagemRepository:
    def listar(self):
        with conectar() as con:
            return [Mensagem(r["nome"], r["email"], r["texto"], r["data"], r["id"])
                    for r in con.execute("SELECT * FROM mensagens ORDER BY id DESC")]

    def buscar(self, id):
        with conectar() as con:
            r = con.execute("SELECT * FROM mensagens WHERE id = ?", (id,)).fetchone()
        return Mensagem(r["nome"], r["email"], r["texto"], r["data"], r["id"]) if r else None

    def salvar(self, m):
        m.validar()
        with conectar() as con:
            if m.id is None:
                m.id = con.execute("INSERT INTO mensagens (nome, email, texto) VALUES (?, ?, ?)",
                                   (m.nome, m.email, m.texto)).lastrowid
            else:
                con.execute("UPDATE mensagens SET nome=?, email=?, texto=? WHERE id=?",
                            (m.nome, m.email, m.texto, m.id))

    def excluir(self, id):
        with conectar() as con:
            con.execute("DELETE FROM mensagens WHERE id = ?", (id,))
