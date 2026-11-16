"""UsuarioRepository: operações SQL da tabela usuarios."""
from database.conexao import conectar
from models.usuario import Usuario


class UsuarioRepository:
    def buscar_por_email(self, email):
        with conectar() as con:
            r = con.execute("SELECT * FROM usuarios WHERE email = ?",
                            ((email or "").strip().lower(),)).fetchone()
        return Usuario(r["nome"], r["email"], r["tipo"], r["senha_hash"], r["id"]) if r else None

    def obter_ou_criar_cliente(self, nome, email):
        """Se o e-mail já existe usa o usuário; senão cadastra um novo cliente."""
        existente = self.buscar_por_email(email)
        if existente:
            return existente
        u = Usuario(nome, email)
        u.validar()
        with conectar() as con:
            u.id = con.execute("INSERT INTO usuarios (nome, email, tipo) VALUES (?, ?, 'cliente')",
                               (u.nome, u.email)).lastrowid
        return u
