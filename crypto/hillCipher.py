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
        list = []
        for j in range(colunasM):
            list.append(matriz[i][j] % valor)
        matrizmod.append(list)
    return matrizmod

def transformaEmLetra(matriz):
    alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
    linhasM = len(matriz)
    colunasM = len(matriz[0])
    matrizNova = []
    for i in range(linhasM):
        for j in range(colunasM):
            matrizNova.insert(matriz[i][j], alfabeto[matriz[i][j]])
    return matrizNova

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
    divisao = [matrizNova[i:i + 2] for i in range(0, len(matrizNova), 2)]
    return divisao


def transporMatriz(m):
    mT = []
    for i in range(len(m)):
        list = []
        for j in range(len(m[0])):
            list.append(m[j][i])
        mT.append(list)
    return mT


def hillCipher(p, k):
    p = list(p.upper())
    divisao = [p[i:i + 2] for i in range(0, len(p), 2)]
    pNum = transformaEmNumero(divisao)
    mult = matrixMultiplication(k, pNum)

    multMod = pmodulo(mult, 26)
    result = transformaEmLetra(multMod)
    return result


c = hillCipher('sixs', matrizA)
c2 = hillCipher('even', matrizA)
print(c, c2)