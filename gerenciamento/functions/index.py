import random
from mysql.connector import Error
import gerenciamento.infra.database
def inicio():
    while True:
        option = int(input("Escolha qual área deseja acessar:\n1-Gerenciamento\n2-Votação\n3-Encerrrar Programa"))
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




def menu():
    a = 0
    while not a == 6:
        a = int(input("Escolha uma opção:\n1-Cadastrar eleitor\n2-Buscar eleitor\n3-Remover eleitor\n4-Editar eleitor\n5-Listar eleitor\n6- Sair\n"))
        match a:
            case 1: 
                cadastrar_eleitor()
                #POST
            case 2:
                buscar_eleitor(gerenciamento.infra.database.conexao)
                #SELECT
            case 3:
                remover_eleitor(gerenciamento.infra.database.conexao)
                #DELETE
            case 4:
                editar_eleitor()
                #UPDATE
                pass
            case 5:
                gerenciamento.infra.database.listar_usuarios()
                #GET OU SELECT
                pass
            case 6:
                print("Voltando...")
                break
            case _:
                print("Opcão Inválida")
 

def cadastrar_eleitor():
        nome = input("Digite o nome: ")
        cpf = input("Digite o cpf: ")
        titulo_eleitor = input("Digite o titulo: ")
        mesario = input("É mesario? (y/n)")
        chave_acesso = "123456"
        sobrenome = nome.split(" ")
        chave_acesso =  nome[0:2].upper() + sobrenome[1][0].upper()  + str(random.randint(1000,9999))
        if mesario == 'y':
            mesario = True
        else:
            mesario = False
        if validar_cpf(cpf):
            gerenciamento.infra.database.post_eleitor(nome, cpf, titulo_eleitor, mesario, chave_acesso) 
            return print(f"Usuario cadastrado com sucesso\nNome: {nome}\nCPF: {cpf}\nChave de Acesso: {chave_acesso}")
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
        campo = "cpf"
        valor = cpf

    else:
        if opcao == "2":
            titulo = input("Digite o título de eleitor (apenas números): ")
            campo = "titulo"
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
        valor = input("Digite o CPF (apenas números): ")
        if not validar_cpf(valor):
            print("CPF inválido.")
            return
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
        valor = input("Digite o CPF (apenas números): ")
        if not validar_cpf(valor):
            print("CPF inválido.")
            return
        campo = "cpf"

    else:
        if opcao == "2":
            valor = input("Digite o título de eleitor (apenas números): ")
            campo = "titulo"

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
