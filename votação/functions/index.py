def menu():
    a = 0
    while not a == 6:
        a = int(input("Escolha uma opção:\n1-Abrir Votação\n2-Auditoria Do Sistema de Votação\n3-Resultado da Votação\n4-Sair\n"))
        match a:
            case 1: 
                print("\n")
                # Abrir Votacao
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

menu()