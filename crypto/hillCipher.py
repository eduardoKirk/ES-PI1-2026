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
            matrizNova.append(alfabeto[matriz[i][j]])
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


c = hillCipher('abra', matrizA)

print(c)

def matrixAdj(m):
    mAdj = []
    for i in range(len(m)):
        list = []
        for j in range(len(m[0])):
            list.append(0)
        mAdj.append(list)
    mAdj[0][0] = m[1][1]
    mAdj[0][1] = int(-m[0][1]) % 26
    mAdj[1][0] = int(-m[1][0]) % 26
    mAdj[1][1] = m[0][0]

    return mAdj

def determinante(m):
    det = (m[0][0] * m[1][1])-(m[0][1] * m[1][0])
    return det

def inversoDet(det):
    a = [1, 3 ,5, 9, 11, 15, 17, 19, 21, 23]
    aInverso = [1, 9, 21, 15, 3, 19, 7, 23, 11, 5, 17]
    for i in range(len(a)):
        if det == a[i]:
            detInverso = aInverso[i]
    return detInverso

def matrizxnum(num, matriz):
    linhas= len(matriz)
    colunas = len(matriz[0])
    for i in range(linhas):
        for j in range(colunas):
            matriz[i][j] = matriz[i][j] * num
    return matriz

def decifrar(k, c):
    detK = determinante(k)
    inversoDetK = inversoDet(detK)
    kAdj = matrixAdj(k)
    mult = matrizxnum(inversoDetK, kAdj)
    kInverso = pmodulo(mult, 26)
    
    c = list(c.upper())
    cNum = transformaEmNumero(c)
    cNumT = transporMatriz(cNum)
    p = matrixMultiplication(kInverso, cNumT)
    pMod = pmodulo(p, 26)
    palavra = transformaEmLetra(pMod)
    palavra = [palavra[i:i+2] for i in range(0, len(palavra), 2)]
    palavra = transporMatriz(palavra)
    palavra = sum(palavra, [])
    return palavra

print(decifrar(matrizA, 'ijed'))