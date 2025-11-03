import os
from cdmm_functions import *

def menu_principal():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n========== Sistema CDMM ==========")
        print("=  1. Usuários                   =")                 
        print("=  2. Categorias                 =")
        print("=  3. Fornecedores               =")
        print("=  4. Produtos                   =")
        print("=  5. Pedidos                    =")
        print("=  6. Movimentações de Estoque   =")
        print("=  0. Sair                       =")
        print("==================================")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            menu_usuarios()
        elif opcao == "2":
            menu_categorias()
        elif opcao == "3":
            menu_fornecedores()
        elif opcao == "4":
            menu_produtos()
        elif opcao == "5":
            menu_pedidos()
        elif opcao == "6":
            menu_estoque()
        elif opcao == "0":
            print("Saindo... Obrigado por usar o CDMM - Management")
            break
        else:
            print("Opção inválida!")
            input("\nPressione 'Enter' para continuar...")

if __name__ == "__main__":
    menu_principal()