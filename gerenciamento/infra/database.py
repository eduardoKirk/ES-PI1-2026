import mysql.connector
# conexao = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='Aqua162318##',
#     database='pi'
# )
conexao = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='Senharuim1@',
    database='pi',
    auth_plugin='mysql_native_password',
    connection_timeout=5
)
# conexao = mysql.connector.connect(
#     host='BD-ACD',
#     port=3306,
#     user='BD12022677',
#     password='Qugqz7',
#     database='BD12022677',
# )
try:
    cursor = conexao.cursor()
    cursor.execute("SELECT VERSION()")
    versao = cursor.fetchone()
    print(f"Conexão bem-sucedida! Versão do MySQL: {versao[0]}")
except mysql.connector.Error as error:
    print(f"Erro ao conectar: {error}")


def listar_usuarios():
    cursor.execute("SELECT id, nome FROM eleitores")
    for(id, nome) in cursor.fetchall():
        print(f"ID: {id} Nome: {nome}\n")


def post_eleitor(nome, cpf, titulo_eleitor, mesario, chave_acesso):
    cursor = conexao.cursor() 
    sql = "INSERT INTO eleitores(nome, cpf, titulo_eleitor, mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
    values = (nome, cpf, titulo_eleitor, mesario, chave_acesso)
    
    cursor.execute(sql, values)
    conexao.commit()
    cursor.close() 

def conta_votos():
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM candidatos;")
    infos = cursor.fetchall()
    for (id, nome) in infos:
        cursor.execute(f"""
            SELECT nome, COUNT(*) 
            FROM votos 
            WHERE id_candidato = {id}
            GROUP BY nome
            ORDER BY nome ASC
        """)
        print(f"Nome: {nome}, votos: {cursor.fetchall()[0][0]}")

