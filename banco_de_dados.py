import sqlite3
from datetime import datetime, date
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
    try:
        con = conexao_banco()
        cursor = con.cursor()
        cursor.execute(insert)
        con.commit()
        con.close()
        print("Inserido com sucesso")
    except Error as error:
        print(error)

def atualizar(update):
    try:
        con = conexao_banco()
        cursor = con.cursor()
        cursor.execute(update)
        con.commit()
        con.close()
        print("Atualizado com sucesso")
    except Error as error:
        print(error)

def deletar(delete):
    try:
        con = conexao_banco()
        cursor = con.cursor()
        cursor.execute(delete)
        con.commit()
        con.close()
        print("Removido com sucesso")
    except Error as error:
        print(error)

def consultar(consultar):
    try:
        con = conexao_banco()
        cursor = con.cursor()
        cursor.execute(consultar)
        valores = cursor.fetchall()
        con.close()
        return valores
    except Error as error:
        print(error)

def consultar_cargos(consultar):
    try:
        con = conexao_banco()
        cursor = con.cursor()
        cursor.execute(consultar)
        dados = cursor.fetchall()
        dados = " ".join("".join(var) for var in dados)
        return dados
    except Error as error:
        print(error)

def consultar_candidatos(consultar):
    try:
        con = conexao_banco()
        cursor = con.cursor()
        cursor.execute(consultar)
        dados = cursor.fetchall()
        if str(dados) == "[(None,)]":
            pass
        else:
            dados = " ".join("".join(var) for var in dados)
            caracteres = '"[]'
            subcaracter = "'"
            for i in range(len(caracteres)):
                dados = dados.replace(caracteres[i],"")
            dados = dados.replace(subcaracter, "")
        return dados
    except Error as error:
        print(error)

def consultar_cpf(consultar):
    try:
        con = conexao_banco()
        cursor = con.cursor()
        cursor.execute(consultar)
        valores = cursor.fetchall()
        #for i in valores:
            #print(i[0])
        con.close()
        return valores
    except Error as error:
        print(error)

def atualizar_data(update):
    try:
        con = conexao_banco()
        cursor = con.cursor()
        cursor.execute(update)
        con.commit()
        con.close()
        print("Atualizado com sucesso")
        return True
    except Error as error:
        print(error)


#data = datetime.today().date().strftime('%d-%m-%Y')
#print(data)

#query = f'SELECT data_inicio FROM eleicao WHERE data_inicio < "{data}";'
#consultar_data(query)

# query = 'INSERT INTO usuario ("nome", "user_name", "senha", "tipo", "status") VALUES ("Elias de Oliveira Cacau", "EliasCacau", "123", "Usuário", 0);'
# query = 'INSERT INTO candidato ("nome", "num_candidato", "votos") VALUES ("Elias de Oliveira Cacau", "4002", 0);'
# inserir(query)

# set = f'UPDATE candidato SET votos="{votos}" WHERE num_candidato LIKE 4002;'
# atualizar(set)

# delete = 'DELETE FROM usuario WHERE id=2;'
# deletar(delete)


#show = 'SELECT user_name, senha FROM usuario;'
#consultar(query)