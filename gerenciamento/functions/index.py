import random
from mysql.connector import Error

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import gerenciamento.infra.database
from crypto.hillCipher import *


def inicio():
    while True:
        option = int(input("Escolha qual área deseja acessar:\n1-Gerenciamento\n2-Votação\n3-Encerrrar Programa\n"))
        match option:
            case 1: 
                print("\n\n")
                menu()
                #Modulo de Gerenciamento
            case 2:
                #Modulo de Votação
                pass
            case 3:
                print("Encerrando programa...")
                gerenciamento.infra.database.cursor.close()
                gerenciamento.infra.database.conexao.close()
                break
            case _:
                print("Opcão Inválida")


chave = [[2, 1], [3, 4]]


def criptografaChave(chave_acesso, matriz):
    p1 = chave_acesso[:3] + chave_acesso[2]

    p1 = hillCipher(p1, matriz)
    p2 = hillCipherNum(chave_acesso[-4:], matriz)
    result = ''
    for i in range(len(p1)):
        for j in range(len(p1[0])):
            result += str(p1[i][j])
            result += str(p2[i][j])

    return result
criptografaChave("ASD1234", chave)

def criptografaCPF(cpf, matriz):
    cpf = cpf + "0"
    print(cpf[8:12])
    p1 = hillCipherNum(cpf[:4], matriz)
    p2 = hillCipherNum(cpf[4:8], matriz)
    p3 = hillCipherNum(cpf[8:12], matriz)
    result = ''
    for i in range(len(p1)):
        for j in range(len(p1[0])):
            result += str(p1[i][j])
            result += str(p2[i][j])
            result += str(p3[i][j])
    return result

def menu():
    a = 0
    while not a == 6:
        a = int(input("Escolha uma opção:\n1-Cadastrar eleitor\n2-Buscar eleitor\n3-Remover eleitor\n4-Editar eleitor\n5-Listar eleitor\n6- Sair\n"))
        match a:
            case 1: 
                print("\n")
                cadastrar_eleitor()
                #POST
            case 2:
                print("\n")
                buscar_eleitor(gerenciamento.infra.database.conexao)
                #SELECT
            case 3:
                print("\n")
                remover_eleitor(gerenciamento.infra.database.conexao)
                #DELETE
            case 4:
                print("\n")
                editar_eleitor()
                #UPDATE
                pass
            case 5:
                print("\n")
                gerenciamento.infra.database.listar_usuarios()
                #GET OU SELECT
                pass
            case 6:
                print("\n")
                print("Voltando...")
                break
            case _:
                print("Opcão Inválida")
 

def cadastrar_eleitor():
        nome = input("Digite o nome: ")
        cpf = input("Digite o cpf: ")
        titulo_eleitor = input("Digite o titulo: ")
        mesario = input("É mesario? (y/n)")
        sobrenome = nome.split(" ")
        chave_acesso =  nome[0:2].upper() + sobrenome[1][0].upper()  + str(random.randint(1000,9999))
        if mesario == 'y':
            mesario = True
        else:
            mesario = False
        if validar_cpf(cpf):
            if validar_titulo(titulo_eleitor):
                 chave_acesso_crypto = criptografaChave(chave_acesso, chave)
                 cpf_crypto = criptografaCPF(cpf, chave)
                 gerenciamento.infra.database.post_eleitor(nome, cpf_crypto, titulo_eleitor, mesario, chave_acesso_crypto) 
                 return print(f"Usuario cadastrado com sucesso\nNome: {nome}\nCPF: {cpf}\nChave de Acesso: {chave_acesso}")
            else:
                return print("Titulo Inválido")
        
        else:
            return print("CPF invalido")

        
        
def validar_cpf(cpf):
    if len(cpf) != 11:
        return False
    else:
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        num1 = 0 if resto < 2 else 11 - resto

        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        num2 = 0 if resto < 2 else 11 - resto

        if str(num1) == cpf[9] and str(num2) == cpf[10]:
            return True
        else:
            return False
            
def validar_titulo(titulo_eleitor):
    if len(titulo_eleitor) != 12:
        return False
    
    n_sequencial = titulo_eleitor[:8]
    uf = titulo_eleitor[8:10]
    dv1p = int(titulo_eleitor[10])
    dv2p = int(titulo_eleitor[11])

    soma = 0
    pesos1 = [2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(8):
        soma += int(n_sequencial[i]) * pesos1[i]
    
    resto = soma % 11
    dv1 = 0 if resto >= 10 else resto

    if uf in ["01", "02"]:
        if resto == 10 or resto == 0:
            dv1 = 1 if resto == 0 else 0 

    soma2 = (int(uf[0]) * 7) + (int(uf[1]) * 8) + (dv1 * 9)
    resto2 = soma2 % 11
    dv2 = 0 if resto2 >= 10 else resto2
    
    if uf in ["01", "02"]:
        if resto2 == 10 or resto2 == 0:
            dv2 = 1 if resto2 == 0 else 0

    return dv1p == dv1 and dv2p == dv2

# Busca eleitor
def buscar_eleitor(conexao):

    print("Buscar eleitor: ")
    print("1- Busca por CPF.")
    print("2- Busca por Titulo de eleitor.")
    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        cpf = input("Digite o CPF do eleitor (apenas números): ")
        if not validar_cpf(cpf):
            print("CPF inválido.")
            return
        cpf_crypto = criptografaCPF(cpf, chave)
        campo = "cpf"
        valor = cpf_crypto

    else:
        if opcao == "2":
            titulo = input("Digite o título de eleitor (apenas números): ")
            campo = "titulo_eleitor"
            valor = titulo

        else:
            print("Opção inválida.")
            return

    try:
        cursor = conexao.cursor(dictionary=True)

        
        sql_busca = "SELECT * FROM eleitores WHERE " + campo + " = %s"
        cursor.execute(sql_busca, (valor,))
        eleitor = cursor.fetchone()
        cursor.close()

        
        if eleitor:
            print("\nEleitor encontrado:")
            print("  Nome:   ", eleitor["nome"])
            print("  CPF:    ", eleitor["cpf"])
            print("  Título: ", eleitor["titulo_eleitor"])

            if eleitor["mesario"] == 1:
                print("  Mesário: Sim")
            else:
                print("  Mesário: Não")

            print("  Status: ", eleitor["status_voto"])

        else:
            print("Nenhum eleitor encontrado com os dados informados.")

    except Error as e:
        print("Erro ao buscar:", e)

# Remover eleitor
def remover_eleitor(conexao):
    print("\nRemover eleitor:")
    print("1 - Buscar por CPF")
    print("2 - Buscar por título de eleitor")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cpf = input("Digite o CPF (apenas números): ")
        if not validar_cpf(cpf):
            print("CPF inválido.")
            return
        cpf_crypto = criptografaCPF(cpf, chave)
        valor = cpf_crypto
        campo = "cpf"

    else:
        if opcao == "2":
            valor = input("Digite o título de eleitor (apenas números): ")
            campo = "titulo_eleitor"

        else:
            print("Opção inválida.")
            return

    try:
        cursor = conexao.cursor(dictionary=True)

        
        sql_busca = "SELECT * FROM eleitores WHERE " + campo + " = %s"
        cursor.execute(sql_busca, (valor,))
        eleitor = cursor.fetchone()

       
        if not eleitor:
            print("Nenhum eleitor encontrado com os dados informados.")
            cursor.close()
            return

        
        print("Eleitor encontrado:")
        print("  Nome:   ", eleitor["nome"])
        print("  CPF:    ", eleitor["cpf"])
        print("  Título: ", eleitor["titulo_eleitor"])

        if eleitor["mesario"] == 1:
            print("  Mesário: Sim")
        else:
            print("  Mesário: Não")

        print("  Status: ", eleitor["status_voto"])

        
        confirmacao = input("\nDeseja realmente remover este eleitor? (s/n): ")

        if confirmacao == "s":
            sql_delete = "DELETE FROM eleitores WHERE " + campo + " = %s"
            cursor.execute(sql_delete, (valor,))
            conexao.commit()
            print("Eleitor removido com sucesso:", eleitor["nome"])
        else:
            print("Remoção cancelada.")

        cursor.close()

    except Error as e:
        print("Erro ao remover:", e)



def editar_eleitor():
    print("\nEditar eleitor:")
    print("1 - Buscar por CPF")
    print("2 - Buscar por título de eleitor")
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        cpf = input("Digite o CPF (apenas números): ")
        if not validar_cpf(cpf):
            print("CPF inválido.")
            return
        cpf_crypto = criptografaCPF(cpf, chave)
        valor = cpf_crypto
        campo = "cpf"
    else:
        if opcao == "2":
            valor = input("Digite o título de eleitor (apenas números): ")
            campo = "titulo_eleitor"

        else:
            print("Opção inválida.")
            return
        
    try:
        cursor = gerenciamento.infra.database.conexao.cursor(dictionary=True)
        
        sql_busca = "SELECT * FROM eleitores WHERE " + campo + " = %s"
        cursor.execute(sql_busca, (valor,))
        eleitor = cursor.fetchone()

        if not eleitor:
            print("Nenhum eleitor encontrado.")
            cursor.close()
            return

        print(f"\nEleitor encontrado: {eleitor['nome']}")


        print("\nDigite os novos dados (deixe vazio para manter os atuais)")
        novo_nome = input("Novo nome: ")
        novo_titulo = input("Novo título: ")
        novo_mesario_input = input("É mesário? (Sim/Não): ")

        
        if novo_nome == "":
            novo_nome = eleitor["nome"]
            
        if novo_titulo == "":
            novo_titulo = eleitor["titulo_eleitor"]

        if novo_mesario_input == "":
            novo_mesario = eleitor["mesario"]
        else:
            novo_mesario = 1 if novo_mesario_input.lower() == "sim" else 0

        sql_update = f"UPDATE eleitores SET nome = %s, titulo_eleitor = %s, mesario = %s WHERE {campo} = %s"
        
        cursor.execute(sql_update, (novo_nome, novo_titulo, novo_mesario, valor))
        gerenciamento.infra.database.conexao.commit()
        
        print("Dados do eleitor atualizados com sucesso!")
        cursor.close()

    except Error as e:
        print("Erro ao atualizar:", e)

        print("\nDigite os novos dados (deixe vazio para manter os atuais)")
        novo_nome = input("Novo nome: ")
        novo_titulo = input("Novo título: ")
        novo_mesario = input("É mesário? (Sim/Não): ")

        if novo_nome == "":
         novo_nome = eleitor["nome"]

         if novo_titulo == "":
          novo_titulo = eleitor["titulo_eleitor"]

        if novo_mesario == "":
            novo_mesario = eleitor["mesario"]
        else:
            if novo_mesario.lower() == "sim":
             novo_mesario = 1
            else:
             novo_mesario = 0


        sql_update = """
        UPDATE eleitores
        SET nome = %s, titulo_eleitor = %s, mesario = %s
        WHERE """ + campo + " = %s"

        cursor.execute(sql_update, (novo_nome, novo_titulo, novo_mesario, valor))
        gerenciamento.infra.database.conexao.commit()

        print("Eleitor atualizado com sucesso")

        cursor.close()

    except Error as e:
            print("Erro ao atualizar:", e)    

inicio()
