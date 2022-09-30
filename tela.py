import tkinter as tk
from tkinter import messagebox
import banco_de_dados as bd
class Tela():
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("500x400")
        self.janela.title("Votação")

        # Login/Cadastro
        self.frm_login = tk.Frame(self.janela)
        self.frm_login.pack(pady=50)

        self.lbl_user = tk.Label(self.frm_login, text="Usuário")
        self.lbl_user.grid(column=0, row=0)
        self.ent_user = tk.Entry(self.frm_login)
        self.ent_user.grid(column=0, row=1)

        self.lbl_null = tk.Label(self.frm_login)
        self.lbl_null.grid(column=0, row=2)

        self.lbl_senha = tk.Label(self.frm_login, text="Senha")
        self.lbl_senha.grid(column=0, row=3)
        self.ent_senha = tk.Entry(self.frm_login, show="*")
        self.ent_senha.grid(column=0, row=4)

        self.lbl_null1 = tk.Label(self.frm_login)
        self.lbl_null1.grid(column=0, row=5)

        self.btn_login = tk.Button(self.frm_login, text="Entrar", command=self.login)
        self.btn_login.grid(column=0, row=6, columnspan=1)

        self.btn_cadastro = tk.Button(self.frm_login, text="Cadastre-se", command=self.cadastro)
        self.btn_cadastro.grid(column=0, row=7, pady=20)

        # Funções
    def login(self):
        user = self.ent_user.get()
        senha = self.ent_senha.get()
        if user == "":
            messagebox.showinfo("Insira um nome", "O campo nome está vazio!")
        elif senha == "":
            messagebox.showinfo("Insira um nome de usuário", "O campo nome de usuário está vazio!")
        else:
            query = 'SELECT user_name, senha FROM usuario;'
            valores = bd.consultar(query)
            logado = False
            for i in valores:
                if i[0] == user and i[1] == senha:
                    logado = True
            if logado:
                messagebox.showinfo("Logado", "Logado com sucesso!!!")
            else:
                messagebox.showinfo("Dados incorretos", "Usuário ou senha incorreto(s)")

    def cadastro(self):
        self.cadastro = tk.Toplevel()
        self.cadastro.geometry("300x220")
        self.lbl_nome = tk.Label(self.cadastro, text="Nome")
        self.lbl_nome.pack()
        self.ent_nome = tk.Entry(self.cadastro)
        self.ent_nome.pack()

        self.lbl_cpf = tk.Label(self.cadastro, text="CPF")
        self.lbl_cpf.pack()
        self.ent_cpf = tk.Entry(self.cadastro)
        self.ent_cpf.pack()

        self.lbl_senha = tk.Label(self.cadastro, text="Senha")
        self.lbl_senha.pack()
        self.ent_senha = tk.Entry(self.cadastro, show="*")
        self.ent_senha.pack()

        self.lbl_con_senha = tk.Label(self.cadastro, text="Confirmar senha")
        self.lbl_con_senha.pack()
        self.ent_con_senha = tk.Entry(self.cadastro, show="*")
        self.ent_con_senha.pack()

        self.btn_con_cadastro = tk.Button(self.cadastro, text="Confirmar", command=self.confirma_cadastro)
        self.btn_con_cadastro.pack(pady=10)

    def confirma_cadastro(self):
        nome = self.ent_nome.get()
        cpf = self.ent_cpf.get()
        senha = self.ent_senha.get()
        con_senha = self.ent_con_senha.get()
        if nome == "" or nome.isnumeric:
            messagebox.showinfo("Insira um nome", "O campo nome está incorreto!")
            self.cadastro.deiconify()
        elif len(cpf) != 11:
            messagebox.showinfo("Insira o cpf", "O campo CPF está incorreto!")
            self.cadastro.deiconify()
        elif not cpf.isnumeric():
            messagebox.showinfo("Insira apenas numeros", "Insira apenas numeros no campo CPF!")
            self.cadastro.deiconify()
        elif senha == "":
            messagebox.showinfo("Insira uma senha", "O campo senha está vazio!")
            self.cadastro.deiconify()
        elif con_senha == "":
            messagebox.showinfo("Confirme a senha", "O campo de confirmação da senha está vazio!")
            self.cadastro.deiconify()
        elif senha != con_senha:
            messagebox.showinfo("Senhas divergentes", "As senhas não correspondem")
            self.cadastro.deiconify()
        else:
            query = 'SELECT cpf FROM usuario;'
            valores = bd.consultar_cpf(query)
            confirmar = False
            for i in valores:
                if cpf == i[0]:
                    confirmar = True
                    break
            if not confirmar:
                query = f'INSERT INTO usuario ("nome", "senha", "tipo", "eleicao_votada", "cpf") VALUES ("{nome}", "{senha}", "Usuário", "[]", "{cpf}");'
                bd.inserir(query)
                messagebox.showinfo("SUCESSO!", "Usuário criado com sucesso!")
                self.cadastro.destroy()
            else:
                messagebox.showinfo("Nome de usuário existente", "Nome de usuário já existente!")
                self.cadastro.destroy()

app = tk.Tk()
Tela(app)
app.mainloop()
