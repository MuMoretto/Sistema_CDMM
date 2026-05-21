# 📦 CDMM — Sistema de Gerenciamento de Estoque

Sistema de estoque desenvolvido em Python com interface CLI e banco de dados MySQL.

**Trabalho Acadêmico** · Ciência da Computação · UNISAGRADO · Bauru - SP

---

## Visão Geral

O **CDMM (Central de Distribuição e Gerenciamento de Materiais)** gerencia de forma integrada usuários, produtos, fornecedores, pedidos e movimentações de estoque, com geração de relatórios analíticos.

---

## Funcionalidades

| Módulo | Operações |
|---|---|
| Usuários | Cadastro, listagem, edição, exclusão |
| Categorias | CRUD completo + edição isolada de descrição |
| Fornecedores | CRUD completo |
| Produtos | CRUD com SKU, preço, estoque e status ativo/inativo |
| Pedidos | Criação, acompanhamento e gestão de status |
| Movimentações | Entradas, saídas e ajustes de estoque com rastreabilidade |
| Relatórios | Estoque por categoria, pedidos por fornecedor, produtos sem estoque, mais vendidos |

---

## Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.8+ | Linguagem principal |
| MySQL | 5.7+ | Banco de dados relacional |
| mysql-connector-python | 8.0+ | Driver MySQL |
| python-dotenv | 0.19+ | Variáveis de ambiente |

---

## Pré-requisitos

- [Python 3.8+](https://www.python.org/downloads/)
- [MySQL Server](https://downloads.mysql.com/archives/community/)
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) *(opcional)*

---

## Instalação

### 1. Clonar e criar ambiente virtual

```bash
# Linux/macOS
python3 -m venv venv && source venv/bin/activate

# Windows
python -m venv venv && venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar banco de dados

Execute o script SQL para criar o schema e dados iniciais:

```bash
mysql -u root -p < database/schema.sql
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=sistema_cdmm
```

### 5. Executar

```bash
python main.py
```

---

## Uso

O sistema apresenta menus interativos no terminal:

```
========== Sistema CDMM ==========
=  1. Usuários                   =
=  2. Categorias                 =
=  3. Fornecedores               =
=  4. Produtos                   =
=  5. Pedidos                    =
=  6. Movimentações de Estoque   =
=  7. Relatórios de Consulta     =
=  0. Sair                       =
==================================
```

---

## Estrutura do Projeto

```
CDMM_System/
├── main.py                     # Ponto de entrada
├── requirements.txt
├── .env.example
│
├── db/
│   └── connection.py           # Conexão e context manager de transações
│
├── models/                     # Regras de negócio e acesso a dados
│   ├── user.py
│   ├── categories.py
│   ├── fornec.py
│   ├── products.py
│   ├── orders.py
│   └── stock_movement.py
│
├── controllers/
│   └── cdmm_functions.py       # Orquestração dos menus
│
├── views/
│   └── cdmm_menu.py            # Interface CLI
│
├── reports/
│   └── reports.py              # Queries analíticas
│
├── database/
│   └── schema.sql              # DDL completo com triggers, procedures e dados iniciais
│
├── docs/
│   ├── ARQUITETURA.md
│   ├── BANCO_DADOS.md
│   └── DECISOES_TECNICAS.md
│
└── tests/
    ├── conftest.py
    ├── test_usuario.py
    ├── test_pedido.py
    ├── test_forecedor.py
    └── test_stock_movement.py
```

---

## Banco de Dados

O schema inclui 7 tabelas, índices, views, triggers e stored procedures:

```
usuarios ──< pedidos ──< itens_pedido >── produtos >── categorias
                                               │
                                    estoque_movimentacoes
                                               │
                                          fornecedores
```

Destaques do schema:
- Trigger `trg_verifica_estoque_before_insert_item` — bloqueia inserção se estoque insuficiente
- Trigger `trg_after_delete_item_pedido` — reverte estoque ao excluir item de pedido
- Procedure `sp_criar_pedido` — cria pedido com itens em transação atômica
- View `vw_pedidos_resumo` — resumo de pedidos com dados do usuário

---

## Testes

```bash
# Instalar pytest
pip install pytest

# Executar todos os testes
pytest

# Executar um arquivo específico
pytest tests/test_pedido.py -v
```

Os testes unitários usam mocks do `Transaction` para não depender de banco de dados real.

---

## Segurança

- **Prepared statements** — prevenção contra SQL Injection
- **Transações ACID** — integridade garantida via context manager com commit/rollback automático
- **Validação em camadas** — validação em Python e constraints no banco
- **Variáveis de ambiente** — credenciais fora do código-fonte

---

## Solução de Problemas

**Erro de conexão com o banco**
Verifique se o MySQL está em execução e se as credenciais no `.env` estão corretas. Confirme que o banco `sistema_cdmm` foi criado com o script `database/schema.sql`.

**`ModuleNotFoundError: No module named 'mysql'`**
Execute `pip install mysql-connector-python`.

**`KeyError: 'DB_HOST'`**
O arquivo `.env` não existe ou não está na raiz do projeto. Crie-o com base no `.env.example`.

---

## Equipe

| Nome | Função |
|---|---|
| Carlos Eduardo Rodrigues Silva | Desenvolvedor |
| Daniel Lucarelli Cerri | Desenvolvedor |
| Melck Silva de Oliveira Nascimento | Desenvolvedor |
| Murilo Moretto Marques | Desenvolvedor |

**Orientador:** Prof. Victor Hugo Braguim Canto  
**Instituição:** UNISAGRADO — Universidade Sagrado Coração, Bauru - SP  
**Curso:** Ciência da Computação

---

**Versão:** 1.0.0 · **Última atualização:** Abril de 2026
