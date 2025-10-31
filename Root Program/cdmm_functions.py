import os
from models.user import Usuario

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