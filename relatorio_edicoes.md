Relátorio de Edições (CDMM - Management)

MENU  ==  OK

USUÁRIO == OK.

CATEGORIAS == ok



CRUD com SQL parametrizado: Garanta que todas as queries usem %s (sem concatenar strings). == pesquisei e analisei o nosso código e já utilizamos

Código modular (camadas): Separar em repositories/ e services/. = confirmação, pois isso reestruturaria todo o projeto

Transações (BEGIN/COMMIT/ROLLBACK): Criar contexto de transação em db/connection.py. == feito( substitui a uso do get_connection pelo Transaction, simplificando o código e deixando mais robusto o sistema de transação do sistema ao banco )

Consultas complexas (JOIN, SUM, EXISTS): Criar um arquivo reports.py com as queries.

Segurança / desempenho: Adicionar pool e evitar SELECT *.

