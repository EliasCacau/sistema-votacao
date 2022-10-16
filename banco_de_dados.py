import sqlite3
from sqlite3 import Error
import os

def conexao_banco():
    dir = os.path.dirname(__file__)
    caminho = f"{dir}/sistema_votacao.db"
    con = None
    try:
        con = sqlite3.connect(caminho)
        return con
    except Error as error:
        print(error)

def inserir(insert):
    con = conexao_banco()
    cursor = con.cursor()
    cursor.execute(insert)
    con.commit()
    con.close()
    print("Inserido com sucesso")

def atualizar(update):
    con = conexao_banco()
    cursor = con.cursor()
    cursor.execute(update)
    con.commit()
    con.close()
    print("Atualizado com sucesso")

def deletar(delete):
    con = conexao_banco()
    cursor = con.cursor()
    cursor.execute(delete)
    con.commit()
    con.close()
    print("Removido com sucesso")

def consultar(consultar):
    con = conexao_banco()
    cursor = con.cursor()
    cursor.execute(consultar)
    valores = cursor.fetchall()
    con.close()
    return valores

def consultar_cargos(consultar):
    con = conexao_banco()
    cursor = con.cursor()
    cursor.execute(consultar)
    dados = cursor.fetchall()
    dados = " ".join("".join(var) for var in dados)
    return dados

def consultar_cpf(consultar):
    con = conexao_banco()
    cursor = con.cursor()
    cursor.execute(consultar)
    valores = cursor.fetchall()
    #for i in valores:
        #print(i[0])
    con.close()
    return valores

# query = 'INSERT INTO usuario ("nome", "user_name", "senha", "tipo", "status") VALUES ("Elias de Oliveira Cacau", "EliasCacau", "123", "Usuário", 0);'
# query = 'INSERT INTO candidato ("nome", "num_candidato", "votos") VALUES ("Elias de Oliveira Cacau", "4002", 0);'
# inserir(query)

# set = f'UPDATE candidato SET votos="{votos}" WHERE num_candidato LIKE 4002;'
# atualizar(set)

# delete = 'DELETE FROM usuario WHERE id=2;'
# deletar(delete)
query = 'SELECT DISTINCT nome_cargo FROM cargo;'
consultar_cargos(query)

#show = 'SELECT user_name, senha FROM usuario;'
#consultar(query)