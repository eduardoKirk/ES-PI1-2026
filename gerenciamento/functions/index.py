import gerenciamento.infra.database
def menu():
    a = 0
    while not a == 6:
        a = int(input("escolha uma opção:\n1-cadastrar eleitor\n2-buscar eleitor\n3-remover eleitor\n4-editar eleitor\n5-listar eleitor\n6- Sair\n"))
        match a:
            case 1: 
                cadastrar_eleitor()
                #POST
            case 2:
                buscar_eleitor(gerenciamento.infra.database.conexao) # buscar_eleitor()
                #SELECT
                pass
            case 3:
                remover_eleitor(gerenciamento.infra.database.conexao) # remover_eleitor()
                #DELETE
                pass
            case 4:
                editar_eleitor() # editar_eleitor()
                #UPDATE
                pass
            case 5:
                # listar_eleitor()
                #GET OU SELECT
                pass
            case 6:
                print("Encerrando programa...")
                gerenciamento.infra.database.cursor.close()
                gerenciamento.infra.database.conexao.close()
                break      
 

def cadastrar_eleitor():
        nome = input("Digite o nome: ")
        cpf = input("Digite o cpf: ")
        titulo_eleitor = input("Digite o titulo: ")
        mesario = input("É mesario? (y/n)")
        chave_acesso = "123456" #Teste
        if mesario == 'y':
            mesario = True
        else:
            mesario = False
        if validar_cpf(cpf):
            gerenciamento.infra.database.post_eleitor(nome, cpf, titulo_eleitor, mesario, chave_acesso) 
            return print(f"Usuario cadastrado com sucesso\nnome: {nome}\ncpf: {cpf}")
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

# Busca um eleitor pelo CPF ou Titulo de eleitor. Dados provinientes do Banco de dados.
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
            print("  Título: ", eleitor["titulo"])

            if eleitor["mesario"] == 1:
                print("  Mesário: Sim")
            else:
                print("  Mesário: Não")

            print("  Status: ", eleitor["status"])

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
            campo = "titulo"

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
        print("  Título: ", eleitor["titulo"])

        if eleitor["mesario"] == 1:
            print("  Mesário: Sim")
        else:
            print("  Mesário: Não")

        print("  Status: ", eleitor["status"])

        
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

# Editar Eleitor
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
        cursor = conexao.cursor(dictionary=True)

        
        sql_busca = "SELECT * FROM eleitores WHERE " + campo + " = %s"
        cursor.execute(sql_busca, (valor,))
        eleitor = cursor.fetchone()

        if not eleitor:
                    print("Nenhum eleitor encontrado com os dados informados.")
                    cursor.close()
                    return
        
        print("\nEleitor encontrado:")
        print("  Nome:   ", eleitor["nome"])
        print("  CPF:    ", eleitor["cpf"])
        print("  Título: ", eleitor["titulo"])
        
        if mesario:
            print("  Mesário:  Sim")
        else:
            print("  Mesário:  Não")

        print("\nDigite os novos dados (deixe vazio para mantar os dados atuais)")

        novo_nome = input("Novo nome:")
        novo_titulo = input("Novo título")
        novo_mesario = input("É mesário? se sim, digite Sim")

        if novo_nome == "":
            novo_nome = eleitor["nome"]

        if novo_titulo == "":
            novo_titulo = eleitor["titulo"]

        if novo_mesario == "":
            novo_mesario = eleitor["mesario"]
        else:
            if novo_mesario == "Sim":
                True
            else:
                False

        sql_update = """
        UPDATE eleitores
        SET nome = %s, titulo = %s, mesario = %s
        WHERE """ + campo + " = %s"

        cursor.execute(sql_update, (novo_nome, novo_titulo, novo_mesario, valor))
        conexao.commit()

        print("Eleitor atualizado com sucesso")

        cursor.close()

        except Error as e:
        print("Erro ao atualizar:", e)

menu()
