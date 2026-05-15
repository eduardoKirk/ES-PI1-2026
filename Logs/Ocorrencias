from datetime import datetime

ARQUIVO_LOG = "ocorrencias.txt"


def registrar(mensagem):
    
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linha = f"[{agora}] {mensagem}\n"

    arquivo = open(ARQUIVO_LOG, "a", encoding="utf-8")
    arquivo.write(linha)
    arquivo.close()


def log_abertura():
  
    registrar("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")


def log_acesso_negado():
   
    registrar("ALERTA: Tentativa de acesso negado")


def log_voto_duplo():
    
    registrar("ALERTA: Tentativa de voto duplo")


def log_voto_sucesso():
    
    registrar("SUCESSO: Voto realizado com sucesso")


def log_encerramento():
    
    registrar("ENCERRAMENTO: Votação finalizada com sucesso.")


def exibir_logs():
    
    print("\n===== LOGS DE OCORRÊNCIAS =====")

    try:
        arquivo = open(ARQUIVO_LOG, "r", encoding="utf-8")
        conteudo = arquivo.read()
        arquivo.close()

        if conteudo:
            print(conteudo)
        else:
            print("Nenhum evento registrado ainda.")

    
    except FileNotFoundError:
        print("Arquivo de log não encontrado. Nenhum evento foi registrado.")

    print("================================\n")
