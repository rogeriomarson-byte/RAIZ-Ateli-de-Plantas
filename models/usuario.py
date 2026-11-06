"""Classe Usuario: cliente da loja ou administrador."""
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario:
    def __init__(self, nome, email, tipo="cliente", senha_hash=None, id=None):
        self.id = id
        self.nome = (nome or "").strip()
        self.email = (email or "").strip().lower()
        self.tipo = tipo
        self._senha_hash = senha_hash       # atributo protegido: a senha nunca é guardada pura

    def definir_senha(self, senha):
        self._senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return bool(self._senha_hash) and check_password_hash(self._senha_hash, senha)

    def eh_admin(self):
        return self.tipo == "admin"

    def validar(self):
        if not self.nome:
            raise ValueError("Informe o seu nome.")
        if "@" not in self.email or "." not in self.email:
            raise ValueError("Informe um e-mail válido.")
