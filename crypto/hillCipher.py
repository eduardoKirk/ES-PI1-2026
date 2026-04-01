matrizA = [[2, 1], 
           [3, 4]]
matrizB = [[16], 
           [5]] 

def matrixMultiplication(a, b):
    linhasA= len(a)
    colunasA = len(a[0])
    linhasB = len(b)
    colunasB = len(b[0])
    if colunasA != linhasB:
        return print('matrizes não podem ser multiplicadas')
    #criar matriz com quantidade de linhas = linhasA e colunas = colunasB
    matrizResultado = []
    for i in range(linhasA):
        linha = []
        for j in range(colunasB):
            soma = 0
            for k in range(colunasA):
                soma += a[i][k] * b[k][j]
            linha.append(soma)
        matrizResultado.append(linha)

    return matrizResultado

def pmodulo(matriz, valor):
    linhasM = len(matriz)
    colunasM = len(matriz[0])
    matrizmod = []
    for i in range(linhasM):
        for j in range(colunasM):
            matrizmod.insert(matriz[i][j], [matriz[i][j] % valor])
    return matrizmod

def alfabeto(matriz):
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
    linhasM = len(matriz)
    colunasM = len(matriz[0])
    matrizNova = []
    for i in range(linhasM):
        for j in range(colunasM):
            matrizNova.insert(matriz[i][j], alfabeto[matriz[i][j]-1])

def transformaEmNumero(matriz):
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
    linhasM = len(matriz)
    colunasM = len(matriz[0])
    matrizNova = []

    for i in range(linhasM):
        for j in range(colunasM):
                for w in range(len(alfabeto)):
                    if matriz[i][j] == alfabeto[w]:
                        matrizNova.append(w)
    n = 2
    divisao = [matrizNova[i:i + n] for i in range(0, len(matrizNova), n)]
    return divisao

def hillCipher(p, k):
    p = list(p.upper())
    n = 2
    divisao = [p[i:i + n] for i in range(0, len(p), n)]
    pNum = transformaEmNumero(divisao)

    for i in range(len(pNum)):
        pNum1 = pNum[i]
        mult = matrixMultiplication(pNum1, k)
        lista =[]
        lista.append(mult)
    print(lista)
    # cpmod = pmodulo(mult, 26)
    # c = alfabeto(cpmod)
    # return c
# c = hillCipher('pene', matrizA)
# print(c)

m1 = [[1],[2],[3]]
m = [[1, 2, 3]]
result = matrixMultiplication(m1, m)
print(result)
