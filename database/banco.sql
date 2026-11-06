-- Banco de dados: raiz.db  (RAIZ - Ateliê de Plantas)
PRAGMA foreign_keys = ON;

CREATE TABLE usuarios (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    senha_hash TEXT,                                   -- só o administrador tem senha
    tipo       TEXT NOT NULL DEFAULT 'cliente' CHECK (tipo IN ('admin', 'cliente'))
);

CREATE TABLE plantas (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      TEXT NOT NULL,
    descricao TEXT NOT NULL,
    preco     REAL NOT NULL CHECK (preco > 0),
    luz       TEXT NOT NULL CHECK (luz IN ('Sol pleno', 'Meia-sombra', 'Pouca luz')),
    agua      TEXT NOT NULL CHECK (agua IN ('Pouca', 'Moderada', 'Muita')),
    cuidados  TEXT NOT NULL,
    imagem    TEXT NOT NULL DEFAULT 'padrao.svg',
    estoque   INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
    destaque  INTEGER NOT NULL DEFAULT 0 CHECK (destaque IN (0, 1))
);

CREATE TABLE pedidos (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    data       TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    total      REAL NOT NULL,
    status     TEXT NOT NULL DEFAULT 'Recebido'
               CHECK (status IN ('Recebido', 'Em preparo', 'Enviado', 'Entregue', 'Cancelado'))
);

-- Um pedido tem vários itens; cada item aponta para uma planta (relação N:N resolvida)
CREATE TABLE itens_pedido (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id      INTEGER NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    planta_id      INTEGER NOT NULL REFERENCES plantas(id),
    quantidade     INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario REAL NOT NULL                        -- guarda o preço da hora da compra
);

CREATE TABLE mensagens (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome  TEXT NOT NULL,
    email TEXT NOT NULL,
    texto TEXT NOT NULL,
    data  TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX idx_itens_pedido ON itens_pedido(pedido_id);
CREATE INDEX idx_pedidos_usuario ON pedidos(usuario_id);

-- ===== Dados iniciais =====
-- Administrador: admin@raiz.com  /  senha: admin123
INSERT INTO usuarios (nome, email, senha_hash, tipo) VALUES
 ('Administrador RAIZ', 'admin@raiz.com', 'scrypt:32768:8:1$e3z3I7gYPGPFh954$96a929cc466ce804ec6d9b083e6f392f33ffc34f94f23f205bd91fae08c65d61b29be363a85a48b88212dd0a3eb1b1838dd76b2c43ff6c5e5c68cc99e297c3be', 'admin'),
 ('Maria Oliveira', 'maria@exemplo.com', NULL, 'cliente');

INSERT INTO plantas (nome, descricao, preco, luz, agua, cuidados, imagem, estoque, destaque) VALUES
 ('Samambaia', 'Folhagem volumosa e delicada, perfeita para dar frescor à sala.', 49.90, 'Meia-sombra', 'Muita', 'Mantenha o solo sempre úmido, borrife água nas folhas e evite sol direto.', 'samambaia.svg', 12, 1),
 ('Costela-de-adão', 'Folhas grandes e recortadas que combinam com ambientes modernos.', 79.90, 'Meia-sombra', 'Moderada', 'Regue quando a terra estiver seca na superfície e limpe as folhas com pano úmido.', 'costela-de-adao.svg', 8, 1),
 ('Jiboia', 'Resistente e pendente, ótima para quem está começando.', 34.90, 'Meia-sombra', 'Moderada', 'Regue uma vez por semana. Pode ser cultivada em vaso ou pendurada.', 'jiboia.svg', 15, 1),
 ('Espada-de-são-jorge', 'Folhas altas e firmes, aguenta cantos de pouca luz.', 44.90, 'Pouca luz', 'Pouca', 'Regue a cada 15 dias e nunca deixe água acumulada no vaso.', 'espada-de-sao-jorge.svg', 10, 0),
 ('Echeveria', 'Suculenta em formato de rosa, ocupa pouco espaço.', 19.90, 'Sol pleno', 'Pouca', 'Regue apenas quando a terra estiver completamente seca. Precisa de bastante luz.', 'echeveria.svg', 20, 0),
 ('Zamioculca', 'Folhas brilhantes e muito resistente, ideal para apartamentos.', 69.90, 'Pouca luz', 'Pouca', 'Regue a cada 2 semanas. Tolera esquecimentos e ambientes internos.', 'zamioculca.svg', 6, 0),
 ('Lavanda', 'Planta aromática de flores roxas que perfuma a casa.', 29.90, 'Sol pleno', 'Moderada', 'Gosta de sol e de solo bem drenado. Regue quando a terra secar.', 'lavanda.svg', 14, 0),
 ('Peperômia', 'Pequena e charmosa, boa para mesas e estantes.', 27.90, 'Meia-sombra', 'Moderada', 'Regue pouco, com a terra quase seca entre as regas. Evite sol forte.', 'peperomia.svg', 9, 0),
 ('Cacto-coluna', 'Cacto resistente que cresce em formato de coluna.', 24.90, 'Sol pleno', 'Pouca', 'Regue uma vez por mês e deixe no sol. Excesso de água apodrece a raiz.', 'cacto.svg', 11, 0);

INSERT INTO pedidos (usuario_id, total, status) VALUES (2, 89.70, 'Recebido');
INSERT INTO itens_pedido (pedido_id, planta_id, quantidade, preco_unitario) VALUES
 (1, 3, 2, 34.90),
 (1, 5, 1, 19.90);

INSERT INTO mensagens (nome, email, texto) VALUES
 ('Carlos Mendes', 'carlos@exemplo.com', 'Olá! Vocês entregam plantas em apartamentos pequenos? Quero uma jiboia.');
