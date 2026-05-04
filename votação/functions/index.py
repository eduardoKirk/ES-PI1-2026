from mysql.connector import Error
import random
import string
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.utils import criptografaCPF, criptografaChave,descriptografaCPF, chave
import gerenciamento.infra.database
from crypto.hillCipher import *

def menu():
    a = 0
    while not a == 6:
        a = int(input("Escolha uma opção:\n1-Abrir Votação\n2-Auditoria Do Sistema de Votação\n3-Resultado da Votação\n4-Sair\n"))
        match a:
            case 1: 
                print("\n")
                abrirSistemaVotacao(gerenciamento.infra.database.conexao)
            case 2:
                print("\n")
                #Auditoria do sistema
            case 3:
                print("\n")
                #resultados
            case 4:
                print("\n")
                print("Voltando...")
                break
            case _:
                print("Opcão Inválida")

def abrirSistemaVotacao(conexao):
    titulo_eleitor = input("Digite o titulo de eleitor: ")
    cpf = input("Digite os primeiros 4 digitos do seu CPF: ")
    chave_acesso = input("Digite a chave de acesso: ")

    try:
        chave_acesso_crypto = criptografaChave(chave_acesso, chave)
        cursor = conexao.cursor(dictionary=True)

        sql_busca = f"SELECT * FROM eleitores WHERE titulo_eleitor = '{titulo_eleitor}'"
        cursor.execute(sql_busca)
        eleitor = cursor.fetchone()

    except Error as e:
        print(e)

    eleitor_cpf = descriptografaCPF(eleitor['cpf'], chave)

    if eleitor['chave_acesso'] == chave_acesso_crypto and eleitor_cpf[:4] == cpf:

        if eleitor['mesario'] == 1:
            print("Abrir processo\n\n")
        else:
            print("Você não tem permissão para abrir o sistema de votação\n\n")

    else:
        print("CPF ou chave de acesso inválidos\n\n")

if __name__ == '__main__':
    menu()


#Protocolo de Votação
letras = "".join(random.choices(string.ascii_uppercase, k=2))
protocolo = "V" + letras + "26" + "17" + str(random.randint(10000,99999))
# 17 = candidato_num[0,1]
print(protocolo)