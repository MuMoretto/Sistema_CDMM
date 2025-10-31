import os
from models.user import Usuario
from models.categories import Categoria 

def menu_usuarios():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")
    while True:
        print("\n--- Usuários ---")
        print("1. Cadastrar usuário")
        print("2. Listar usuários")
        print("3. Editar usuário")
        print("4. Excluir usuário")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            user = Usuario(nome, email, telefone)
            user.salvar()
        elif opcao == "2":
            Usuario.listar()
        elif opcao == "3":
            id_usuario = input("ID do usuário que deseja editar: ")
            novo_nome = input("Novo nome: ")
            novo_email = input("Novo email: ")
            novo_telefone = input("Novo telefone: ")
            Usuario.editar(id_usuario, novo_nome, novo_email, novo_telefone)
        elif opcao == "4":
            id_usuario = input("ID do usuário que deseja excluir: ")
            Usuario.excluir(id_usuario)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_categorias():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")

    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")
    while True:
        print("\n--- Categoria ---")
        print("1. Cadastrar Categoria de produto")
        print("2. Listar Categorias")
        print("3. Editar Categoria")
        print("4. Excluir Categoria")
        print("5. editar descricao")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            descricao = input("Descricao: ")
            categori = Categoria(nome, descricao)
            categori.salvar()
            
        elif opcao == "2":
            Categoria.listar()

        elif opcao == "3":
            id_categoria = input("ID da categoria a ser editada: ")
            novo_nome = input("Novo nome da categoria: ")
            nova_descricao = input("Nova descrição da categoria: ")
            Categoria.editar(id_categoria, novo_nome, nova_descricao)

        elif opcao == "4":
            id_categoria = input("ID da categoria a ser excluída:")
            Categoria.excluir(id_categoria)

        elif opcao == "5":
            id_categoria = input("ID da categoria a ser editada: ")
            nova_descricao = input("Nova descrição da categoria: ")
            Categoria.editar_descricao(id_categoria, nova_descricao)
            
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def menu_fornecedores():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")

def menu_produtos():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")

def menu_pedidos():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")

def menu_estoque():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")