# RAIZ — Ateliê de Plantas

Projeto Integrado do 2º ano — Curso Técnico em Informática (Colégio UNASP-HT) · **DWS + POO + BD**.
Loja virtual de plantas: catálogo, carrinho, pedidos, contato e área administrativa.

## Como executar
```bash
pip install -r requirements.txt
python app.py          # abra http://127.0.0.1:5000
```
O banco `database/raiz.db` é criado sozinho, com dados de exemplo, a partir de `database/banco.sql`.\n\n**Importante:** não abra os arquivos HTML com dois cliques. Inicie o Flask pelo terminal e acesse o endereço `http://127.0.0.1:5000`. As fotos do catálogo carregam pela internet; se uma foto não carregar, o sistema mostra a ilustração local correspondente.

**Área administrativa:** http://127.0.0.1:5000/login — e-mail `admin@raiz.com`, senha `admin123`.

## Estrutura
```
RAIZ/
├── app.py                  rotas Flask (páginas + API usada pelo JavaScript)
├── config.py               caminhos e chave da sessão
├── database/               conexao.py (SQLite) e banco.sql (tabelas + dados iniciais)
├── models/                 classes: Planta, Usuario, Pedido, ItemPedido, Mensagem, Carrinho
├── repositories/           SQL de cada tabela: Planta, Usuario, Pedido, Mensagem
├── templates/              páginas HTML (Jinja2)
├── static/css, js, img     estilos, JavaScript (Fetch) e imagens
└── docs/                   diagramas, apresentação e guia de commits
```

## Como DWS, POO e BD se integram
1. O navegador abre uma página (HTML/CSS) ou o JavaScript chama uma rota `/api/...` com **Fetch**.
2. A rota em `app.py` cria objetos das **classes** (`Planta`, `Pedido`...) e chama um **repository**.
3. O repository executa **SQL** no SQLite e devolve objetos para a rota, que responde com HTML ou JSON.

## Como testar cada operação
| Operação | Onde testar |
|---|---|
| Inserir planta | Admin → Plantas → *Cadastrar nova planta* |
| Consultar | Catálogo (busca e filtro de luz) e detalhes de cada planta |
| Atualizar | Admin → Plantas → *Editar* (ou mudar o status de um pedido) |
| Excluir | Admin → *Excluir* (planta já vendida não pode ser excluída: zere o estoque) |
| Pedido | Adicione plantas ao carrinho → informe nome e e-mail → *Finalizar pedido* → veja em Admin → Pedidos |
| Mensagem | Contato → enviar → Admin → Mensagens (editar e excluir) |
| Persistência | Pare o servidor (Ctrl+C), rode de novo: os dados continuam |

## Decisões do projeto
- Banco **SQLite** (arquivo único, sem instalar nada).
- O carrinho fica na sessão do navegador; ao finalizar, o pedido e os itens vão para o banco e o estoque é baixado.
- Clientes não têm login: o e-mail informado no pedido cria (ou reaproveita) um registro em `usuarios`.
- As imagens do cadastro de plantas são escolhidas entre os arquivos da pasta `static/img`.
