from mysql.connector import Error

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from gerenciamento.functions.index import gerenciamento_menu
from votação.functions.index import votacao_menu

def inicio():
    while True:
        option = int(input("Escolha qual área deseja acessar:\n1-Gerenciamento\n2-Votação\n3-Encerrrar Programa\n\nEscolha uma opção: "))
        match option:
            case 1: 
                print("\n\n")
                gerenciamento_menu()
            case 2:
                print("\n\n")
                votacao_menu()
            case 3:
                print("Encerrando programa...")
                break
            case _:
                print("Opcão Inválida")

inicio()