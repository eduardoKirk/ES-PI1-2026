
def menu():
    a = 0
    while not a == 6:
        a = int(input("escolha uma opção:\n1-cadastrar eleitor\n2-buscar eleitor\n3-listar eleitor\n4-remover celeitor\n5-editar eleitor\n6- Sair\n"))
        match a:
            case 1: 
                cadastrar_eleitor()
                #POST
            case 2:
                # buscar_eleitor()
                #SELECT
                menu()
            case 3:
                # remover_eleitor()
                #DELETE
                menu()
            case 4:
                # editar_eleitor()
                #UPDATE
                menu()
            case 5:
                # listar_eleitor()
                #GET OU SELECT
                menu()
            case 6:
                print("Encerrando programa...")
                break      
 

def cadastrar_eleitor():
        nome = input("digite o nome: ")
        cpf = input("digite o cpf: ")
        titulo = input("digite o titulo: ")
        mesario = input("É mesario? (y/n)")
        chave_acesso = "123456" #Teste
        if mesario == 'y':
            mesario = True
        else:
            mesario = False
        if validar_cpf(cpf):
            # post_eleitor(nome, cpf, titulo, mesario, chave_acesso) 
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
        
menu()
