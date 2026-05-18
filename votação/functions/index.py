from mysql.connector import Error
import random
import string
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.utils import criptografaCPF, criptografaChave, criptografaProtocolo,descriptografaCPF, chave
import gerenciamento.infra.database
from gerenciamento.infra.database import conta_votos
from crypto.hillCipher import *
from Logs.ocorrencias import log_abertura, log_acesso_negado, log_voto_duplo, log_voto_sucesso, log_encerramento, exibir_logs


def fecharVotacao(conexao):
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
                    log_encerramento()
                    return 0  # VotacaoAberta = 0
                else:
                    print("Chave de acesso incorreta. Encerramento cancelado.")
                    log_acesso_negado()

            else:
                print("Encerramento cancelado. Voltando ao menu anterior.")
    
        else:
            print("Você não tem permissão para encerrar o sistema de votação\n\n")
            log_acesso_negado()
    else:
        print("CPF ou chave de acesso inválidos\n\n")
        log_acesso_negado()

def votacao_menu():
    a = 0
    while not a == 6:
        a = int(input("Escolha uma opção:\n1-Abrir Votação\n2-Auditoria Do Sistema de Votação\n3-Resultado da Votação\n4-Fechar Votação\n5- Sair\n\nEscolha uma opção: "))
        match a:
            case 1: 
                print("\n")
                abrirSistemaVotacao(gerenciamento.infra.database.conexao)
            case 2:
                print("\n")
                exibir_logs()
            case 3:
                print("\n")
                #resultados
            case 4:
                print("\n")
                fecharVotacao(gerenciamento.infra.database.conexao)
                #FecharVotacao
                break
            case 5:
                print("Saindo...")
                # inicio()
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
            AbrirVotacao = input("Digite sim para começar o processo\n")
    
            if AbrirVotacao == 'sim':
                print("Abrindo processo de votação: ")
                
                try:
                    cursor = conexao.cursor()
                    cursor.execute("TRUNCATE TABLE votos")
                    cursor.execute("UPDATE eleitores SET status_voto = 0 WHERE id < 9999")
                    # cursor.execute("UPDATE votos SET status_voto = true")
                    
                    conexao.commit()

                    print("""
                          ---------------------------
                          Votação aberta com sucesso!
                          ---------------------------\n\n""")
                    log_abertura()
                    conta_votos()
                    
                except Error as e:
                    print(e)

                print("Escolha uma opção: \n1-Votação\n2-Encerrar Sistema de Votação")
                a = input("")
                match a:
                    case '1':
                        votacao()
                    case '2':
                        fecharVotacao()
                    case _:
                        print("Opcão Inválida")

            else:
                print("Processo não iniciado, voltando a página inicial")
                AbrirVotacao = 'n'
                votacao_menu()

        else:
            print("Você não tem permissão para abrir o sistema de votação\n\n")
            log_acesso_negado()

    else:
        print("CPF ou chave de acesso inválidos\n\n")
        log_acesso_negado()

def votacao(conexao):
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

    if eleitor is None:
        print("CPF ou chave de acesso inválidos\n\n")
        log_acesso_negado()
        votacao_menu()
        return
    else: 
        eleitor_cpf = descriptografaCPF(eleitor['cpf'], chave)

    if eleitor['chave_acesso'] == chave_acesso_crypto and eleitor_cpf[:4] == cpf:
        if eleitor['status_voto'] == 1:
            print("Você ja realizou o voto.")
            log_voto_duplo()
            votacao_menu()
            
        else:
            confirmacao = 'n'
            while confirmacao == 'n':
                print("Digite o número do candidato")
                num_canditado = int(input(""))
                try:
                    cursor = conexao.cursor(dictionary=True)
                    sql_busca = f"SELECT nome, numero, partido, id FROM candidatos WHERE numero={num_canditado};"
                    cursor.execute(sql_busca)
                    candidato = cursor.fetchone()
                except Error as e:
                    print(e)
                print(f"""
                    NOME: {candidato['nome']}       NUMERO: {candidato['numero']}       PARTIDO: {candidato['partido']}  
                    """)
                print("Confirmar voto? s/n")
                confirmacao = input("")
                if confirmacao == 's':
                    try:
                        agora = datetime.now()
                        letras = "".join(random.choices(string.ascii_uppercase, k=2))
                        protocolo = "V" + letras + "26" + str(num_canditado) + str(random.randint(10000,99999))
                        protocolo_crypto = criptografaProtocolo(protocolo, chave)
                        sql_busca = f"""INSERT INTO votos(id_candidato, id_eleitor, data_hora, protocolo) VALUES 
                        ({candidato['id']}, {eleitor['id']}, '{agora.strftime('%Y-%m-%d %H:%M:%S')}', '{protocolo_crypto}'); """
                        cursor.execute(sql_busca)
                        conexao.commit()
                        cursor.close()
                        log_voto_sucesso()

                        print(f"PROTOCOLO: {protocolo}")
            
                    except Error as e:
                        print(e)
    else:
        print("CPF ou chave de acesso inválidos\n\n")
        log_acesso_negado()
        votacao_menu()
        return
    
def resultado_votacao():
    options = 0
    while not options == 6:
        options = int(input("Escolha uma opção:\n1-Boletim de Urna\n2-Auditoria Do Sistema de Votação\n3-Resultado da Votação\n4-Fechar Votação\n5- Sair\n\nEscolha uma opção: "))
        match a:
            case 1: 
                print("\n")
                boletim_urna()
            case 2:
                print("\n")
                exibir_logs()
            case 3:
                print("\n")
            case _:
                print("Opcão Inválida")

def boletim_urna():
    try:
        cursor = conexao.cursor()

        sql_buscando = f"""SELECT c.nome, c.numero, c.partido, COUNT (v.id_voto)AS total_votos
        FROM candidatos c LEFT JOIN voto v ON c.id_candidato = v.id_candidato
        GROUP BY c.id_candidato, c.nome, c.numero, c.partido ORDER BY c.nome ASC"""
        cursor.execute(sql_buscando)
        resultados = cursor.fetchall()

        print("\nBoletim de Urna")
        print(f"{'CANDIDATO':<30} {'NÚMERO':<10} {'PARTIDO':<10} {'VOTOS'}")

        for linha in resultados:
            nome, numero, partido, total_votos = linha
            print(f"{nome:<30} {numero:<10} {partido:<10} {total_votos}")
        
        sql_vencedor = """
            SELECT c.nome, c.numero, c.partido, COUNT(v.id_voto) AS total_votos
            FROM candidatos c
            LEFT JOIN voto v ON v.id_eleitor = c.id_candidato
            GROUP BY c.id_candidato, c.nome, c.numero, c.partido
            ORDER BY total_votos DESC
            LIMIT 1
        """

        cursor.execute(sql_vencedor)
        vencedor = cursor.fetchone()

        if vencedor:
            nome, numero, partido, total_votos = vencedor
            print("\n Vencedor")
            print(f"  Nome:         {nome}")
            print(f"  Número:       {numero}")
            print(f"  Partido:      {partido}")
            print(f"  Total Votos:  {total_votos}")

        cursor.close()
    except Error as e:
        print(e)

# votacao(gerenciamento.infra.database.conexao)
# votacao_menu()

# boletim_urna()
