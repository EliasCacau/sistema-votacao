import tkinter as tk
from tkinter import messagebox, ttk, Menu
import banco_de_dados as bd
import bcrypt

class Tela():
    def __init__(self, master):
        mestre = master
        self.janela = master
        self.janela.geometry("500x400")
        self.janela.title("Votação")
        # self.janela.configure(bg="White")

        self.user_logged = ''

        # Login/Cadastro
        self.frm_login = tk.Frame(self.janela)
        self.frm_login.pack(pady=50)

        self.lbl_cpf = tk.Label(self.frm_login, text="CPF")
        self.lbl_cpf.grid(column=0, row=0)
        self.ent_cpf = tk.Entry(self.frm_login)
        self.ent_cpf.grid(column=0, row=1)

        self.lbl_null = tk.Label(self.frm_login)
        self.lbl_null.grid(column=0, row=2)

        self.lbl_senha = tk.Label(self.frm_login, text="Senha")
        self.lbl_senha.grid(column=0, row=3)
        self.ent_senha = tk.Entry(self.frm_login, show="*")
        self.ent_senha.grid(column=0, row=4)

        self.lbl_null1 = tk.Label(self.frm_login)
        self.lbl_null1.grid(column=0, row=5)

        self.btn_login = tk.Button(self.frm_login, text="Entrar", command=self.login, width=12)
        self.btn_login.grid(column=0, row=6, columnspan=1)

        self.btn_cadastro = tk.Button(self.frm_login, text="Cadastre-se", command=self.cadastro, width=12)
        self.btn_cadastro.grid(column=0, row=7, pady=20)

        self.btn_destroir = tk.Button(self.frm_login, text="VOTE AQUI", command=self.votacao)
        self.btn_destroir.grid(column=1, row=7)

        self.btn_admin = tk.Button(self.frm_login, text="ADMINISTRADOR", command=self.administrador)
        self.btn_admin.grid(column=1, row=8)

        self.menu_bar = Menu(self.janela)
        self.janela.config(menu=self.menu_bar)

        self.config_menu = Menu(self.menu_bar, tearoff=0)
        self.config_menu.add_command(label="Sair", command=self.janela.quit)
        self.menu_bar.add_cascade(label="Configurações", menu=self.config_menu)

        self.button = tk.Button(self.frm_login, text="NOVA JANELA", command=self.nova_janela(self.janela))
        self.button.grid(column=1, row=9)

    def nova_janela(self, master):
        #self.janela.destroy()
        self.nova_janela = master
        self.nova_janela.geometry("800x600")

    # Funções
    def login(self):
        cpf = self.ent_cpf.get()
        senha = self.ent_senha.get().encode("utf-8")
        if cpf == "":
            messagebox.showinfo("Insira o cpf", "O campo cpf está vazio!")
        elif senha == "":
            messagebox.showinfo("Insira a senha", "O campo senha está vazio!")
        else:
            query = 'SELECT cpf, senha, id senha FROM usuario;'
            valores = bd.consultar(query)
            logado = False
            for i in valores:
                if i[0] == cpf:
                    hash = i[1][2:len(i[1])-1].encode("utf-8")
                    if bcrypt.checkpw(senha, hash):
                        logado = True
                        self.user_logged = i[2]
            if logado:
                # messagebox.showinfo("Logado", "Logado com sucesso!!!")
                if self.user_logged == 12:
                    print(self.user_logged)
                    self.administrador()
                else:
                    self.votacao()
            else:
                messagebox.showinfo("Dados incorretos", "Usuário ou senha inválido")

    def cadastro(self):
        self.cadastro = tk.Toplevel()
        self.cadastro.geometry("300x250")
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

        self.lbl_sexo = tk.Label(self.cadastro, text="Sexo")
        self.lbl_sexo.pack()
        self.cbx_sexo = ttk.Combobox(self.cadastro, width=17)
        self.cbx_sexo['values'] = ('Masculino', 'Feminino', 'Indefinido')
        self.cbx_sexo.pack()

        self.btn_con_cadastro = tk.Button(self.cadastro, text="Confirmar", command=self.confirma_cadastro)
        self.btn_con_cadastro.pack(pady=10)

    def confirma_cadastro(self):
        nome = self.ent_nome.get()
        cpf = self.ent_cpf.get()
        senha = self.ent_senha.get().encode('utf-8')
        con_senha = self.ent_con_senha.get().encode('utf-8')
        sexo = self.cbx_sexo.get()

        # Criptografando a senha
        salt = bcrypt.gensalt(8)
        senha = bcrypt.hashpw(senha, salt)
        con_senha = bcrypt.hashpw(con_senha, salt)

        if nome == "":
            messagebox.showinfo("Insira um nome", "O campo nome está incorreto!")
            self.cadastro.deiconify()
        #elif len(cpf) != 11:
        elif cpf == "":
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
            #senha = senha[2:62]
            for i in valores:
                if cpf == i[0]:
                    confirmar = True
                    break
            if not confirmar:
                query = f'INSERT INTO usuario ("nome", "senha", "tipo", "eleicao_votada", "cpf", "sexo") VALUES ("{nome}", "{senha}", "Usuário", "[]", "{cpf}", "{sexo}");'
                bd.inserir(query)
                messagebox.showinfo("SUCESSO!", "Usuário criado com sucesso!")
                self.cadastro.destroy()
            else:
                messagebox.showinfo("CPF já cadastrado", "O CPF já cadastrado no servidor!")
                self.cadastro.destroy()

    def administrador(self):
        self.admin = tk.Toplevel()
        self.admin.geometry("800x600")
        self.admin.title("Administrador")

        self.lbl_titulo = tk.Label(self.admin, text="Candidatos", font=32)
        self.lbl_titulo.pack()

        self.frm_candidato = tk.Frame(self.admin)
        self.frm_candidato.pack()

        self.lbl_nome = tk.Label(self.frm_candidato, text='Nome:')
        self.lbl_nome.grid(row=0, column=0)
        self.ent_nome = tk.Entry(self.frm_candidato, width=40)
        self.ent_nome.grid(row=0, column=1)

        self.btn_inserir = tk.Button(self.frm_candidato, text='Inserir', command=self.inserir_cadidato)
        self.btn_inserir.grid(row=1, column=1, sticky=tk.E)

        self.tvw = ttk.Treeview(self.frm_candidato, columns=('id', 'nome'), show='headings')
        self.tvw.column('id', width=40)
        self.tvw.column('nome', width=150)
        self.tvw.heading('id', text='Id')
        self.tvw.heading('nome', text='Nome')
        self.tvw.grid(row=3, column=0, columnspan=3)
        self.atualizar_tvw()

    def atualizar_tvw(self):
        for i in self.tvw.get_children():
            self.tvw.delete(i)
        query = 'SELECT * FROM candidato;'
        dados = bd.consultar(query)
        for tupla in dados:
            self.tvw.insert('', tk.END, values=tupla)

    def inserir_cadidato(self):
        nome = self.ent_nome.get()
        if nome == '':
            messagebox.showwarning('Aviso', 'Insira um nome!')
        else:
            sql = f'INSERT INTO candidato ("nome") VALUES("{nome}");'
            bd.inserir(sql)
            self.atualizar_tvw()
            messagebox.showinfo('Aviso', 'Cliente inserido com sucesso!')
            self.ent_nome.delete(0, 'end')

    def votacao(self):
        self.votar = tk.Toplevel(self.janela)
        self.votar.geometry("800x600")
        self.votar.title("Área de votos")


app = tk.Tk()
Tela(app)
app.mainloop()
