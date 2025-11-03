DROP DATABASE IF EXISTS sistema_cdmm;
CREATE DATABASE sistema_cdmm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sistema_cdmm;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefone VARCHAR(30) NOT NULL UNIQUE,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (CHAR_LENGTH(nome) > 1)
);

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao VARCHAR(255),
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fornecedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    contato VARCHAR(150),
    UNIQUE (nome)
);

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    sku VARCHAR(50) UNIQUE,
    id_categoria INT,
    id_fornecedor INT,
    preco DECIMAL(12,2) NOT NULL CHECK (preco >= 0),
    quantidade_estoque INT NOT NULL DEFAULT 0 CHECK (quantidade_estoque >= 0),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    data_pedido DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_pedido DECIMAL(12,2) NOT NULL CHECK (total_pedido >= 0),
    status ENUM('em_andamento','concluido','cancelado') NOT NULL DEFAULT 'em_andamento',
    observacao VARCHAR(255),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE itens_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(12,2) NOT NULL CHECK (preco_unitario >= 0),
    subtotal DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produtos(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_subtotal CHECK (ABS(subtotal - (quantidade * preco_unitario)) < 0.01)
);

CREATE TABLE estoque_movimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_produto INT NOT NULL,
    tipo_movimentacao ENUM('entrada','saida','ajuste') NOT NULL,
    quantidade INT NOT NULL,
    data_movimentacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    referencia VARCHAR(100),
    observacao VARCHAR(255),
    FOREIGN KEY (id_produto) REFERENCES produtos(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_produtos_nome ON produtos(nome);
CREATE INDEX idx_produtos_categoria ON produtos(id_categoria);
CREATE INDEX idx_pedidos_usuario ON pedidos(id_usuario);
CREATE INDEX idx_itens_pedido_pedido ON itens_pedido(id_pedido);

CREATE VIEW vw_pedidos_resumo AS
SELECT
  p.id AS pedido_id,
  p.data_pedido,
  p.status,
  u.id AS usuario_id,
  u.nome AS usuario_nome,
  p.total_pedido
FROM pedidos p
JOIN usuarios u ON p.id_usuario = u.id;

DROP FUNCTION IF EXISTS calcular_total_pedido;
DELIMITER $$
CREATE FUNCTION calcular_total_pedido(p_id INT) RETURNS DECIMAL(12,2)
DETERMINISTIC
BEGIN
    DECLARE tot DECIMAL(12,2) DEFAULT 0;
    SELECT IFNULL(SUM(subtotal),0) INTO tot FROM itens_pedido WHERE id_pedido = p_id;
    RETURN tot;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_criar_pedido;
DELIMITER $$
CREATE PROCEDURE sp_criar_pedido(
    IN p_id_usuario INT,
    IN p_items JSON,
    OUT p_new_pedido_id INT
)
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE tmp_id_prod INT;
    DECLARE tmp_qt INT;
    DECLARE tmp_pre DECIMAL(12,2);
    DECLARE tmp_sub DECIMAL(12,2);
    DECLARE i INT DEFAULT 0;
    DECLARE arr_len INT DEFAULT JSON_LENGTH(p_items);

    START TRANSACTION;

    INSERT INTO pedidos (id_usuario, total_pedido, status) VALUES (p_id_usuario, 0.00, 'em_andamento');
    SET p_new_pedido_id = LAST_INSERT_ID();

    WHILE i < arr_len DO
        SET tmp_id_prod = JSON_EXTRACT(p_items, CONCAT('$[', i, '].id_produto'));
        SET tmp_qt = JSON_EXTRACT(p_items, CONCAT('$[', i, '].quantidade'));
        SET tmp_pre = JSON_EXTRACT(p_items, CONCAT('$[', i, '].preco_unitario'));
        SET tmp_sub = tmp_qt * tmp_pre;

        INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario, subtotal)
        VALUES (p_new_pedido_id, tmp_id_prod, tmp_qt, tmp_pre, tmp_sub);

        INSERT INTO estoque_movimentacoes (id_produto, tipo_movimentacao, quantidade, referencia, observacao)
        VALUES (tmp_id_prod, 'saida', tmp_qt, CONCAT('pedido#', p_new_pedido_id), NULL);

        UPDATE produtos
          SET quantidade_estoque = quantidade_estoque - tmp_qt
          WHERE id = tmp_id_prod;

        SET i = i + 1;
    END WHILE;

    UPDATE pedidos SET total_pedido = (SELECT IFNULL(SUM(subtotal),0) FROM itens_pedido WHERE id_pedido = p_new_pedido_id)
    WHERE id = p_new_pedido_id;

    COMMIT;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_verifica_estoque_before_insert_item;
DELIMITER $$
CREATE TRIGGER trg_verifica_estoque_before_insert_item
BEFORE INSERT ON itens_pedido
FOR EACH ROW
BEGIN
    DECLARE estoque_atual INT;
    SELECT quantidade_estoque INTO estoque_atual FROM produtos WHERE id = NEW.id_produto FOR UPDATE;
    IF estoque_atual IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Produto inexistente.';
    END IF;
    IF estoque_atual < NEW.quantidade THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Estoque insuficiente para o produto.';
    END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_after_insert_item_pedido;
DELIMITER $$
CREATE TRIGGER trg_after_insert_item_pedido
AFTER INSERT ON itens_pedido
FOR EACH ROW
BEGIN
    INSERT INTO estoque_movimentacoes (id_produto, tipo_movimentacao, quantidade, referencia)
    VALUES (NEW.id_produto, 'saida', NEW.quantidade, CONCAT('item_pedido#', NEW.id));
    UPDATE produtos SET quantidade_estoque = quantidade_estoque - NEW.quantidade WHERE id = NEW.id_produto;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_after_delete_item_pedido;
DELIMITER $$
CREATE TRIGGER trg_after_delete_item_pedido
AFTER DELETE ON itens_pedido
FOR EACH ROW
BEGIN
    INSERT INTO estoque_movimentacoes (id_produto, tipo_movimentacao, quantidade, referencia, observacao)
    VALUES (OLD.id_produto, 'entrada', OLD.quantidade, CONCAT('cancel_item_pedido#', OLD.id_pedido), 'revertido por exclusao de item');
    UPDATE produtos SET quantidade_estoque = quantidade_estoque + OLD.quantidade WHERE id = OLD.id_produto;
END$$
DELIMITER ;

INSERT INTO usuarios (nome, email, telefone) VALUES
('Murilo Moretto', 'murilo@gmail.com', '11111111111'),
('Cliente Teste', 'cliente@hotmail.com', '11111111112');

INSERT INTO categorias (nome, descricao) VALUES
('Verduras', 'Verduras - Alface Crespa, Alface Lisa, Rúcula...'),
('Legumes', 'Legumes - Cenoura, Batata, Mandioca...'),
('Frutas', 'Frutas - Maçã, Pêra, Melancia, Morango...');

INSERT INTO fornecedores (nome, contato) VALUES
('Fornecedor Márcio Batatas', 'contatomarciobatata@gmail.com'),
('Fornecedor Beto Frutis', 'vendas_betofrutis@hotmail.com');

INSERT INTO produtos (nome, sku, id_categoria, id_fornecedor, preco, quantidade_estoque) VALUES
('Alface Americana', 'SKU-001', 1, 1, 12.50, 100),
('Batata Baroa (Mandioquinha)', 'SKU-002', 2, 1, 8.90, 50),
('Banana Nanica', 'SKU-003', 3, 2, 6.00, 200);

INSERT INTO pedidos (id_usuario, total_pedido, status) VALUES (2, 0.00, 'concluido');
SET @pedido_id = LAST_INSERT_ID();
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario, subtotal) VALUES
(@pedido_id, 1, 2, 12.50, 25.00),
(@pedido_id, 3, 1, 6.00, 6.00);
UPDATE pedidos SET total_pedido = (SELECT SUM(subtotal) FROM itens_pedido WHERE id_pedido = @pedido_id) WHERE id = @pedido_id;

ANALYZE TABLE produtos, pedidos, itens_pedido, estoque_movimentacoes;