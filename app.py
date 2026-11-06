"""RAIZ - Ateliê de Plantas: servidor Flask (rotas)."""
import os
import sqlite3
from functools import wraps
from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash, jsonify, abort)
import config
from database.conexao import iniciar
from models.planta import Planta, LUZES, AGUAS
from models.pedido import Pedido, STATUS
from models.mensagem import Mensagem
from models.carrinho import Carrinho
from repositories.planta_repository import PlantaRepository
from repositories.usuario_repository import UsuarioRepository
from repositories.pedido_repository import PedidoRepository
from repositories.mensagem_repository import MensagemRepository

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
iniciar()                                    # cria o banco na primeira vez

repo_plantas = PlantaRepository()
repo_usuarios = UsuarioRepository()
repo_pedidos = PedidoRepository()
repo_mensagens = MensagemRepository()


# ---------- Funções auxiliares ----------
@app.template_filter("brl")
def brl(valor):
    """12.5 -> R$ 12,50"""
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@app.template_filter("img")
def img(nome):
    """Retorna fotografias para o catálogo; mantém SVG local como alternativa."""
    if nome.startswith("http"):
        return nome
    fotos = {
        "samambaia.svg": "https://images.unsplash.com/photo-1497250681960-ef046c08a56e?auto=format&fit=crop&w=1000&q=85",
        "costela-de-adao.svg": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=1000&q=85",
        "jiboia.svg": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1000&q=85",
        "espada-de-sao-jorge.svg": "https://images.unsplash.com/photo-1497250681960-ef046c08a56e?auto=format&fit=crop&w=1000&q=85",
        "echeveria.svg": "https://images.unsplash.com/photo-1509423350716-97f2360af3e4?auto=format&fit=crop&w=1000&q=85",
        "zamioculca.svg": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=1000&q=85",
        "lavanda.svg": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1000&q=85",
        "peperomia.svg": "https://images.unsplash.com/photo-1497250681960-ef046c08a56e?auto=format&fit=crop&w=1000&q=85",
        "cacto.svg": "https://images.unsplash.com/photo-1509423350716-97f2360af3e4?auto=format&fit=crop&w=1000&q=85",
    }
    return fotos.get(nome, url_for("static", filename="img/" + nome))


@app.context_processor
def globais():
    return dict(carrinho_qtd=Carrinho(session).quantidade_total(), eh_admin=session.get("admin", False))


def admin_requerido(funcao):
    @wraps(funcao)
    def interna(*args, **kwargs):
        if not session.get("admin"):
            if request.path.startswith("/api/"):
                return jsonify(erro="Faça login como administrador."), 401
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)
    return interna


def dados_json():
    return request.get_json(force=True) or {}


@app.errorhandler(ValueError)
@app.errorhandler(KeyError)
@app.errorhandler(TypeError)
def erro_dados(e):
    msg = str(e) if isinstance(e, ValueError) else "Dados incompletos ou inválidos."
    return jsonify(erro=msg), 400


@app.errorhandler(sqlite3.IntegrityError)
def erro_integridade(e):
    return jsonify(erro="Este registro está em uso e não pode ser excluído "
                        "(ex.: planta que já foi vendida). Zere o estoque."), 409


# ---------- Páginas públicas ----------
@app.route("/")
def index():
    return render_template("index.html", destaques=repo_plantas.destaques())


@app.route("/plantas")
def plantas():
    busca, luz = request.args.get("q", "").strip(), request.args.get("luz", "")
    return render_template("plantas.html", plantas=repo_plantas.listar(busca, luz),
                           busca=busca, luz=luz, luzes=LUZES)


@app.route("/plantas/<int:id>")
def detalhes(id):
    planta = repo_plantas.buscar(id) or abort(404)
    return render_template("detalhes.html", planta=planta)


@app.route("/carrinho")
def carrinho():
    itens = Carrinho(session).itens(repo_plantas)
    return render_template("carrinho.html", itens=itens, total=sum(i.subtotal for i in itens))


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/pedido/<int:id>")
def pedido_ok(id):
    pedido = repo_pedidos.buscar(id) or abort(404)
    return render_template("pedido_ok.html", pedido=pedido)


# ---------- API (usada pelo JavaScript com Fetch) ----------
@app.post("/api/carrinho/adicionar")
def carrinho_adicionar():
    d = dados_json()
    planta = repo_plantas.buscar(int(d["planta_id"])) or abort(404)
    c = Carrinho(session)
    c.adicionar(planta, int(d.get("quantidade", 1)))
    return jsonify(mensagem=f"{planta.nome} adicionada ao carrinho.", qtd_total=c.quantidade_total())


@app.post("/api/carrinho/alterar")
def carrinho_alterar():
    d = dados_json()
    planta = repo_plantas.buscar(int(d["planta_id"])) or abort(404)
    c = Carrinho(session)
    c.alterar(planta, int(d["quantidade"]))
    return jsonify(mensagem="Carrinho atualizado.", qtd_total=c.quantidade_total())


@app.post("/api/carrinho/remover")
def carrinho_remover():
    c = Carrinho(session)
    c.remover(int(dados_json()["planta_id"]))
    return jsonify(mensagem="Item removido.", qtd_total=c.quantidade_total())


@app.post("/api/pedidos")
def finalizar_pedido():
    d = dados_json()
    c = Carrinho(session)
    itens = c.itens(repo_plantas)
    if not itens:
        raise ValueError("O carrinho está vazio.")
    cliente = repo_usuarios.obter_ou_criar_cliente(d["nome"], d["email"])
    pedido = Pedido(cliente)
    for item in itens:
        pedido.adicionar_item(item)
    id_pedido = repo_pedidos.salvar(pedido)
    c.esvaziar()
    return jsonify(mensagem="Pedido realizado!", pedido_id=id_pedido), 201


@app.post("/api/mensagens")
def enviar_mensagem():
    d = dados_json()
    repo_mensagens.salvar(Mensagem(d["nome"], d["email"], d["texto"]))
    return jsonify(mensagem="Mensagem enviada! Responderemos em breve."), 201


# ---------- Login do administrador ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = repo_usuarios.buscar_por_email(request.form.get("email", ""))
        if usuario and usuario.eh_admin() and usuario.verificar_senha(request.form.get("senha", "")):
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("E-mail ou senha incorretos.", "erro")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


# ---------- Área administrativa ----------
@app.route("/admin")
@admin_requerido
def admin():
    aba = request.args.get("aba", "plantas")
    return render_template("admin.html", aba=aba, status_lista=STATUS,
                           plantas=repo_plantas.listar() if aba == "plantas" else [],
                           pedidos=repo_pedidos.listar() if aba == "pedidos" else [],
                           mensagens=repo_mensagens.listar() if aba == "mensagens" else [])


def planta_do_formulario(id=None):
    f = request.form
    return Planta(f["nome"].strip(), f["descricao"].strip(), f["preco"].replace(",", "."),
                  f["luz"], f["agua"], f["cuidados"].strip(), f.get("imagem") or "padrao.svg",
                  f.get("estoque", 0), "destaque" in f, id)


@app.route("/admin/plantas/nova", methods=["GET", "POST"])
@app.route("/admin/plantas/<int:id>/editar", methods=["GET", "POST"])
@admin_requerido
def planta_form(id=None):
    planta = repo_plantas.buscar(id) if id else None
    if id and not planta:
        abort(404)
    if request.method == "POST":
        try:
            repo_plantas.salvar(planta_do_formulario(id))
            flash("Planta salva com sucesso.", "ok")
            return redirect(url_for("admin", aba="plantas"))
        except ValueError as e:
            flash(str(e), "erro")
    valores = request.form if request.method == "POST" else (planta.dados() if planta else {"estoque": 1})
    pasta = os.path.join(app.static_folder, "img")
    imagens = sorted(a for a in os.listdir(pasta) if a.endswith((".svg", ".png", ".jpg", ".jpeg", ".webp")))
    return render_template("planta_form.html", v=valores, editando=bool(id),
                           luzes=LUZES, aguas=AGUAS, imagens=imagens)


@app.route("/admin/mensagens/<int:id>/editar", methods=["GET", "POST"])
@admin_requerido
def mensagem_form(id):
    msg = repo_mensagens.buscar(id) or abort(404)
    if request.method == "POST":
        try:
            repo_mensagens.salvar(Mensagem(request.form["nome"], request.form["email"],
                                           request.form["texto"], id=id))
            flash("Mensagem atualizada.", "ok")
            return redirect(url_for("admin", aba="mensagens"))
        except ValueError as e:
            flash(str(e), "erro")
    return render_template("mensagem_form.html", m=msg)


@app.delete("/api/admin/plantas/<int:id>")
@admin_requerido
def api_excluir_planta(id):
    repo_plantas.excluir(id)
    return jsonify(mensagem="Planta excluída.")


@app.delete("/api/admin/pedidos/<int:id>")
@admin_requerido
def api_excluir_pedido(id):
    repo_pedidos.excluir(id)
    return jsonify(mensagem="Pedido excluído.")


@app.put("/api/admin/pedidos/<int:id>/status")
@admin_requerido
def api_status_pedido(id):
    repo_pedidos.atualizar_status(id, dados_json()["status"])
    return jsonify(mensagem="Status atualizado.")


@app.delete("/api/admin/mensagens/<int:id>")
@admin_requerido
def api_excluir_mensagem(id):
    repo_mensagens.excluir(id)
    return jsonify(mensagem="Mensagem excluída.")


if __name__ == "__main__":
    app.run(debug=True)
