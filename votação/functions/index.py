from mysql.connector import Error
import random
import string
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.utils import criptografaCPF, criptografaChave, criptografaProtocolo,descriptografaCPF, chave
import gerenciamento.infra.database
from crypto.hillCipher import *


def FecharVotacao(conexao):
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
        return
 
    eleitor_cpf = descriptografaCPF(eleitor['cpf'], chave)
 
    chave_ok = eleitor['chave_acesso'] == chave_acesso_crypto
    cpf_ok = str(eleitor_cpf)[:4] == cpf

    if chave_ok and cpf_ok:
        if eleitor['mesario'] == 1:
            confirmar = input("Deseja realmente encerrar a votação? (Sim/Não): ")
            confirmar = confirmar.lower()
    
            if confirmar == 'sim':    

                #segunda confirmacao da chave:
                chave_confirmacao = input("Digite novamente sua chave de acesso para confirmar: ")
                chave_confirmacao_crypto = criptografaChave(chave_confirmacao, chave)

                if chave_confirmacao_crypto == eleitor['chave_acesso']:
                    print("Votação encerrada com sucesso!")
                    return 0  # VotacaoAberta = 0
                else:
                    print("Chave de acesso incorreta. Encerramento cancelado.")

            else:
                print("Encerramento cancelado. Voltando ao menu anterior.")
    
        else:
            print("Você não tem permissão para encerrar o sistema de votação\n\n")
    else:
        print("CPF ou chave de acesso inválidos\n\n")


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
                FecharVotacao(gerenciamento.infra.database.conexao)
                #FecharVotacao
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
            AbrirVotacao = input("Digite sim para começar o processo")
    
            if AbrirVotacao == 'sim':
                print("Abrindo processo de votação: ")
                
                try:
                    cursor = conexao.cursor()
                    cursor.execute("TRUNCATE TABLE voto")
                    cursor.execute("UPDATE eleitores SET status_votacao = 0 WHERE id < 9999")
                    cursor.execute("UPDATE voto SET abertura_votacao = true")
                    
                    conexao.commit()

                    print("Votação aberta com sucesso!")
                    print("Voltando ao menu principal")
                    
                except Error as e:
                    print(e)

            else:
                print("Processo não iniciado, voltando a página inicial")
                AbrirVotacao = 'n'
                return menu

        else:
            print("Você não tem permissão para abrir o sistema de votação\n\n")

    else:
        print("CPF ou chave de acesso inválidos\n\n")

def FecharVotacao(conexao):
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
            FecharVotacao = input("Digite sim para fechar a votação")
            if FecharVotacao == 'sim':
                VotacaoAberta == 0 

    


#Protocolo de Votação
letras = "".join(random.choices(string.ascii_uppercase, k=2))
protocolo = "V" + letras + "26" + "17" + str(random.randint(10000,99999))
# 17 = candidato_num[0,1]
print(protocolo)
criptografaProtocolo("VRT269950134", chave)


if __name__ == '__main__':
    menu()