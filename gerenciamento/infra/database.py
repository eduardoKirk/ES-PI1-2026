import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Aqua162318##',
    database='pi'
)

try:
    cursor = conexao.cursor()
    cursor.execute("SELECT VERSION()")
    versao = cursor.fetchone()
    print(f"Conexão bem-sucedida! Versão do MySQL: {versao[0]}")
except mysql.connector.Error as error:
    print(f"Erro ao conectar: {error}")


def listar_usuarios():
    cursor.execute("SELECT id, nome, cpf FROM eleitores")
    for(id, nome, cpf) in cursor.fetchall():
        print(f"ID: {id} Nome: {nome} CPF: {cpf}")


def post_eleitor(nome, cpf, titulo_eleitor, mesario, chave_acesso):
    cursor = conexao.cursor() 
    sql = "INSERT INTO eleitores(nome, cpf, titulo_eleitor, mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
    values = (nome, cpf, titulo_eleitor, mesario, chave_acesso)
    
    cursor.execute(sql, values)
    conexao.commit()
    cursor.close() 

