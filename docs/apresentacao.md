# Roteiro de apresentação — RAIZ

**Objetivo.** A RAIZ é uma loja virtual de plantas pensada para iniciantes e para quem mora em apartamento. O cliente vê as plantas, descobre quanta luz e água cada uma precisa, monta o carrinho e faz o pedido. A loja gerencia tudo por uma área administrativa.

**Como o site funciona.** Na página inicial aparecem as plantas em destaque. No catálogo dá para buscar por nome e filtrar por luz, e cada planta tem uma página com os cuidados. No carrinho eu mudo as quantidades, vejo o total e finalizo informando nome e e-mail. Na página de contato o cliente manda mensagem. No admin (login `admin@raiz.com`) eu cadastro, edito e excluo plantas, vejo os pedidos, mudo o status deles e administro as mensagens.

**DWS.** Todo o site: HTML nas páginas da pasta `templates`, CSS em `static/css/style.css` (verde, cards, responsivo para celular) e JavaScript em `static/js/script.js`. O JavaScript usa **Fetch** para adicionar ao carrinho, finalizar pedido, enviar mensagem e excluir sem recarregar tudo. As rotas Flask ficam em `app.py`.

**POO.** As classes ficam na pasta `models`: `Planta`, `Usuario`, `Pedido`, `ItemPedido`, `Mensagem` e `Carrinho`. Usei **encapsulamento**: o preço e o estoque da planta só aceitam valores válidos (setters), e a senha do usuário fica protegida (`_senha_hash`). Um `Pedido` pertence a um `Usuario` e contém vários `ItemPedido` (relacionamento entre classes). Cada tabela tem um **repository** com o SQL (`PlantaRepository`, `PedidoRepository`...), separando a regra do sistema do acesso ao banco.

**Banco de dados.** SQLite, arquivo `database/raiz.db`, criado pelo `banco.sql`. Tabelas: `usuarios`, `plantas`, `pedidos`, `itens_pedido` e `mensagens`. O pedido liga ao usuário por chave estrangeira, e `itens_pedido` liga pedidos e plantas (um pedido tem várias plantas e uma planta aparece em vários pedidos). O preço do item é guardado na hora da compra. Ao finalizar, o pedido e o estoque são gravados juntos: se faltar estoque, nada é gravado.

**Integração.** O navegador (DWS) manda a ação para uma rota Flask, a rota cria objetos das classes (POO) e chama o repository, que roda o SQL no banco (BD) e devolve a resposta. Exemplo: ao finalizar um pedido, o Fetch envia nome e e-mail, a rota monta um `Pedido` com os `ItemPedido` do `Carrinho`, o `PedidoRepository` grava nas tabelas e a tela de confirmação mostra o resultado.

**Principais classes:** Planta, Usuario, Pedido, ItemPedido, Mensagem, Carrinho. **Principais tabelas:** plantas, usuarios, pedidos, itens_pedido, mensagens.

**Para executar e testar:** `pip install -r requirements.txt`, depois `python app.py` e abrir `http://127.0.0.1:5000`. Os passos de teste de cada operação estão no README.
