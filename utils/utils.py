
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import gerenciamento.infra.database
from crypto.hillCipher import *

chave = [[2, 1], [3, 4]]



def criptografaChave(chave_acesso, matriz):
    try:
        p1 = chave_acesso[:3] + chave_acesso[2]

        p1 = hillCipher(p1, matriz)
        p2 = hillCipherNum(chave_acesso[-4:], matriz)
        
        result = ''
        for i in range(len(p1)):
            for j in range(len(p1[0])):
                result += str(p1[i][j])
                result += str(p2[i][j])

        return result
    
    except Exception as e:
        return e


def criptografaCPF(cpf, matriz):
    try:
        cpf = cpf + "0"
        p1 = hillCipherNum(cpf[:4], matriz)
        p2 = hillCipherNum(cpf[4:8], matriz)
        p3 = hillCipherNum(cpf[8:12], matriz)
        t = p1, p2, p3
        string = ''
        for lista in t:
            for letra in lista:
                string += letra
        return string
    except Exception as e:
        return e


def descriptografaCPF(cpf, matriz):
    try:
        cpf = list(cpf)
        result1 = decifrarNum(matriz, cpf[0:4])
        result2 = decifrarNum(matriz, cpf[4:8])
        result3 = decifrarNum(matriz, cpf[8:12])
        t = result1, result2, result3
        string = ''
        for matriz in t:
            for linha in matriz:
                for elemento in linha:
                    string += str(elemento)
        return string

    except Exception as e:
        return e

def criptografaProtocolo(protocolo, matriz):
    try:
        protocolo = protocolo[:3] + 'X' + protocolo[3:] + "000"
        result1 = hillCipher(protocolo[0:4], matriz)
        result2 = hillCipherNum(protocolo[4:8], matriz)
        result3 = hillCipherNum(protocolo[8:12], matriz)
        result4 = hillCipherNum(protocolo[12:16], matriz)
        
        t = result1, result2, result3, result4
        string = ''
        string = ''
        for matriz in t:
            for linha in matriz:
                for elemento in linha:
                    string += str(elemento)
        return string
    except Exception as e:
        return e
    
    

# print(descriptografaCPF('OFVSJQSLVSIM',chave))
# print(criptografaCPF('54854174854', chave))

# print(criptografaChave("EDC2412",chave))

# print(criptografaProtocolo("VRT269950134", chave))