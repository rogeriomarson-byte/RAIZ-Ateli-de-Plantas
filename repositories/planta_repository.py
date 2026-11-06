"""PlantaRepository: todas as operações SQL da tabela plantas."""
from database.conexao import conectar
from models.planta import Planta


class PlantaRepository:
    def listar(self, busca="", luz=""):
        sql, params = "SELECT * FROM plantas WHERE 1=1", []
        if busca:
            sql += " AND (nome LIKE ? OR descricao LIKE ?)"
            params += [f"%{busca}%", f"%{busca}%"]
        if luz:
            sql += " AND luz = ?"
            params.append(luz)
        with conectar() as con:
            return [Planta.de_linha(r) for r in con.execute(sql + " ORDER BY nome", params)]

    def destaques(self):
        with conectar() as con:
            return [Planta.de_linha(r) for r in con.execute(
                "SELECT * FROM plantas WHERE destaque = 1 ORDER BY nome LIMIT 3")]

    def buscar(self, id):
        with conectar() as con:
            r = con.execute("SELECT * FROM plantas WHERE id = ?", (id,)).fetchone()
        return Planta.de_linha(r) if r else None

    def salvar(self, p):
        """INSERT se a planta é nova, UPDATE se já tem id."""
        p.validar()
        valores = (p.nome, p.descricao, p.preco, p.luz, p.agua, p.cuidados,
                   p.imagem, p.estoque, int(p.destaque))
        with conectar() as con:
            if p.id is None:
                p.id = con.execute("""INSERT INTO plantas
                    (nome, descricao, preco, luz, agua, cuidados, imagem, estoque, destaque)
                    VALUES (?,?,?,?,?,?,?,?,?)""", valores).lastrowid
            else:
                con.execute("""UPDATE plantas SET nome=?, descricao=?, preco=?, luz=?, agua=?,
                    cuidados=?, imagem=?, estoque=?, destaque=? WHERE id=?""", (*valores, p.id))

    def excluir(self, id):
        with conectar() as con:
            con.execute("DELETE FROM plantas WHERE id = ?", (id,))
