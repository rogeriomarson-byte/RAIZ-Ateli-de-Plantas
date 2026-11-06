"""Classe Mensagem: mensagem enviada pelo formulário de contato."""


class Mensagem:
    def __init__(self, nome, email, texto, data=None, id=None):
        self.id = id
        self.nome = (nome or "").strip()
        self.email = (email or "").strip()
        self.texto = (texto or "").strip()
        self.data = data

    def validar(self):
        if not (self.nome and self.email and self.texto):
            raise ValueError("Preencha nome, e-mail e mensagem.")
        if "@" not in self.email:
            raise ValueError("Informe um e-mail válido.")
