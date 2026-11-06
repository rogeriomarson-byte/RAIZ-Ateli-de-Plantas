"""Classe Planta: representa uma planta da loja."""
LUZES = ("Sol pleno", "Meia-sombra", "Pouca luz")
AGUAS = ("Pouca", "Moderada", "Muita")


class Planta:
    def __init__(self, nome, descricao, preco, luz, agua, cuidados,
                 imagem="padrao.svg", estoque=0, destaque=False, id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco          # passa pelo setter (validação)
        self.luz = luz
        self.agua = agua
        self.cuidados = cuidados
        self.imagem = imagem
        self.estoque = estoque      # passa pelo setter (validação)
        self.destaque = bool(destaque)

    # --- Encapsulamento: preço e estoque só aceitam valores válidos ---
    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ValueError("Preço inválido.")
        if valor <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        self._preco = round(valor, 2)

    @property
    def estoque(self):
        return self._estoque

    @estoque.setter
    def estoque(self, valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError("Estoque inválido.")
        if valor < 0:
            raise ValueError("O estoque não pode ser negativo.")
        self._estoque = valor

    def disponivel(self):
        return self._estoque > 0

    def validar(self):
        if not (self.nome and self.descricao and self.cuidados):
            raise ValueError("Preencha nome, descrição e cuidados.")
        if self.luz not in LUZES or self.agua not in AGUAS:
            raise ValueError("Escolha uma opção válida de luz e de água.")

    def dados(self):
        """Dicionário usado para preencher formulários."""
        return {"nome": self.nome, "descricao": self.descricao, "preco": self.preco,
                "luz": self.luz, "agua": self.agua, "cuidados": self.cuidados,
                "imagem": self.imagem, "estoque": self.estoque, "destaque": self.destaque}

    @classmethod
    def de_linha(cls, r):
        """Cria um objeto Planta a partir de uma linha do banco."""
        return cls(r["nome"], r["descricao"], r["preco"], r["luz"], r["agua"], r["cuidados"],
                   r["imagem"], r["estoque"], r["destaque"], r["id"])
