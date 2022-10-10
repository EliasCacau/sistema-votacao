import tkinter as tk
from tkinter import messagebox, ttk, Menu
from tkinter import filedialog as fd
import banco_de_dados as bd
import bcrypt
import os
from PIL import Image

class Tela():
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("500x400")
        self.janela.title("Administrador")
        # self.janela.configure(bg="White")
        self.janela.withdraw()
        self.login()
        self.user_logged = ''

        self.menu_bar = tk.Menu(self.janela)
        self.janela.config(menu=self.menu_bar)

        self.cand_menu = Menu(self.menu_bar, tearoff=0)
        self.cand_menu.add_command(label="Adicionar candidato", command=self.inserir_candidatos)
        self.cand_menu.add_command(label="Mostrar candidatos", command=self.candidatos)
        self.menu_bar.add_cascade(label="Candidatos", menu=self.cand_menu)

        self.cargo_menu = Menu(self.menu_bar, tearoff=0)
        self.cargo_menu.add_command(label="Mostrar cargos", command=self.mostrar_cargo)
        self.menu_bar.add_cascade(label="Cargos", menu=self.cargo_menu)

        self.eleicao_menu = Menu(self.menu_bar, tearoff=0)
        self.eleicao_menu.add_command(label="Mostrar eleições", command=self.mostrar_eleicoes)
        self.menu_bar.add_cascade(label="Eleições", menu=self.eleicao_menu)

        self.config_menu = Menu(self.menu_bar, tearoff=0)
        self.config_menu.add_command(label="Sair", command=self.janela.quit)
        self.menu_bar.add_cascade(label="Configurações", menu=self.config_menu)

    def inserir_candidatos(self):
        self.ins_candidato = tk.Toplevel(self.janela)
        self.ins_candidato.title("Inserir candidatos")
        self.ins_candidato.geometry("400x160")
        self.voltar = tk.Button(self.ins_candidato, text="Voltar", command=self.ins_candidato.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)
        self.lbl_titulo = tk.Label(self.ins_candidato, text="Cadastrar Candidato", font=32)
        self.lbl_titulo.pack()

        self.frm_candidato = tk.Frame(self.ins_candidato)
        self.frm_candidato.pack()

        self.lbl_nome = tk.Label(self.frm_candidato, text='Nome do candidato:')
        self.lbl_nome.grid(column=0, row=0, pady=10)
        self.ent_nome = tk.Entry(self.frm_candidato, width=30)
        self.ent_nome.grid(column=1, row=0)

        self.lbl_imagem = tk.Label(self.frm_candidato, text="(Opcional):")
        self.lbl_imagem.grid(column=0, row=1, pady=10)

        self.btn_imagem = tk.Button(self.frm_candidato, text="Selecionar imagem", command=self.imagem_candidato)
        self.btn_imagem.grid(column=1, row=1)

        self.btn_inserir = tk.Button(self.frm_candidato, text='Adicionar Candidato', command=self.inserir_cadidato)
        self.btn_inserir.grid(column=0, row=3, columnspan=2, pady=10)

        self.imagem = ''

    def candidatos(self):
        self.candidatos = tk.Toplevel(self.janela)
        self.candidatos.geometry("400x335")
        self.candidatos.title("Candidatos")
        self.lbl_cand = tk.Label(self.candidatos, text="          Candidatos", font=32)
        self.lbl_cand.pack()
        self.frm_pesq = tk.Frame(self.candidatos)
        self.frm_pesq.pack()
        self.lbl_pesq = tk.Label(self.frm_pesq, text="Pesquisar:")
        self.lbl_pesq.grid(column=0, row=0)
        self.ent_pesq = tk.Entry(self.frm_pesq)
        self.ent_pesq.grid(column=1, row=0)
        self.btn_pesq = tk.Button(self.frm_pesq, text="O", width=3, command=self.pesquisar_tvw_candidato)
        self.btn_pesq.grid(column=2, row=0, padx=3, pady=5)

        self.voltar = tk.Button(self.candidatos, text="Voltar", command=self.candidatos.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)
        self.tvw = ttk.Treeview(self.candidatos, columns=('id', 'nome'), show='headings')
        self.tvw.column('id', width=40)
        self.tvw.column('nome', width=250)
        self.tvw.heading('id', text='Id')
        self.tvw.heading('nome', text='Nome')
        self.tvw.pack()
        self.atualizar_tvw_candidato()

        self.frm_botao = tk.Frame(self.candidatos)
        self.frm_botao.pack()

        self.btn_mostrar = tk.Button(self.frm_botao, text="Ver foto", command=self.mostrar_candidato, width=8)
        self.btn_mostrar.grid(column=0, row=0, padx=2, pady=5)
        self.btn_adc = tk.Button(self.frm_botao, text="Adicionar", command=self.inserir_candidatos, width=8)
        self.btn_adc.grid(column=1, row=0, padx=2)
        self.btn_editar = tk.Button(self.frm_botao, text="Editar", command=self.editar_candidato, width=8)
        self.btn_editar.grid(column=2, row=0, padx=2)
        self.btn_excluir = tk.Button(self.frm_botao, text="Excluir", command=self.excluir_candidato, width=8)
        self.btn_excluir.grid(column=3, row=0, padx=2)

    def editar_candidato(self):
        selecionado = self.tvw.selection()
        lista = self.tvw.item(selecionado, "values")

        self.edit_cand = tk.Toplevel(self.candidatos)
        self.edit_cand.title("Editar candidato")
        self.edit_cand.geometry("300x250")

        self.nome = tk.Label(self.edit_cand, text="Editar candidato", font=32)
        self.nome.pack()

        self.frm_edit = tk.Frame(self.edit_cand)
        self.frm_edit.pack()
        self.lbl_nome = tk.Label(self.frm_edit, text="Nome:")
        self.lbl_nome.grid(column=0, row=0, pady=10)
        self.ent_nome = tk.Entry(self.frm_edit)
        self.ent_nome.grid(column=1, row=0)
        self.ent_nome.insert(0, lista[1])

        self.edit_img = tk.Label(self.frm_edit, text="Editar Imagem:")
        self.edit_img.grid(column=0, row=1)
        self.btn_img = tk.Button(self.frm_edit, text="Selecionar imagem", command=self.edit_imagem_cand)
        self.btn_img.grid(column=1, row=1)

        self.btn_conf_edit = tk.Button(self.frm_edit, text="Confirmar", command=self.confirmar_edit_cand)
        self.btn_conf_edit.grid(column=0, row=2, columnspan=2, pady=10)

        self.nova_img = ''

    def edit_imagem_cand(self):
        tipos = (('Imagem', '*.PNG'), ('Todos', '*.*'))
        self.nova_img = fd.askopenfilename(initialdir='/imgs',
                                         filetypes=tipos)
        self.edit_cand.deiconify()

    def confirmar_edit_cand(self):
        selecionado = self.tvw.selection()
        lista = self.tvw.item(selecionado, "values")
        nome = self.ent_nome.get()
        if nome == "":
            messagebox.showinfo("O campo nome está vazio!")
        else:
            mensagem = messagebox.askyesno("CUIDADO", "Você tem certeza que deseja realizar a(s) alteração(ões)?")
            if mensagem:
                if self.nova_img == '':
                    query = f'UPDATE candidato SET nome="{nome}" WHERE id={lista[0]};'
                    bd.atualizar(query)
                    self.atualizar_tvw_cadidato()
                    self.edit_cand.destroy()
                    self.candidatos.deiconify()
                else:
                    query = f'UPDATE candidato SET nome="{nome}", foto="{self.nova_img}" WHERE id={lista[0]};'
                    bd.atualizar(query)
                    self.atualizar_tvw_cadidato()
                    self.edit_cand.destroy()
                    self.candidatos.deiconify()
            else:
                self.edit_cand.destroy()
                self.candidatos.deiconify()

    def excluir_candidato(self):
        selecionado = self.tvw.selection()
        lista = self.tvw.item(selecionado, "values")
        mensagem = messagebox.askyesno("Excluir", "Você tem certeza que deseja excluir o candidato?")
        if mensagem:
            sql = f'DELETE FROM candidato WHERE id={lista[0]};'
            bd.deletar(sql)
            messagebox.showinfo("Excluído", "Candidato excluído com sucesso")
            self.atualizar_tvw_cadidato()
        self.candidatos.deiconify()

    def imagem_candidato(self):
        tipos = (('Imagem', '*.PNG'), ('Imagem', '*.JPG'), ('Todos', '*.*'))
        self.imagem = fd.askopenfilename(initialdir=f'/imgs',
                                         filetypes=tipos)
        if self.imagem.endswith(".jpg"):
            img = Image.open(f'{self.imagem}')
            self.imagem = self.imagem.replace(".jpg", "")
            img.save(f'{self.imagem}.png')
            os.remove(f'{self.imagem}.jpg')
            self.imagem = f"{self.imagem}.png"
        self.ins_candidato.deiconify()

    def mostrar_candidato(self):
        selecionado = self.tvw.selection()
        if selecionado == ():
            messagebox.showinfo("Selecine candidato", "Selecione um candidato")
            self.candidatos.deiconify()
        else:
            self.candidato = tk.Toplevel(self.janela)
            self.candidato.title("Candidato")
            id = self.tvw.item(selecionado, 'values')[0]
            sql = f"SELECT * FROM candidato WHERE id={id}"
            valor = bd.consultar(sql)
            self.minha_imagem = tk.PhotoImage(file=f"{valor[0][2]}")
            self.lbl_mostrar_cand = tk.Label(self.candidato, image=self.minha_imagem)
            self.lbl_mostrar_cand.image = self.minha_imagem
            self.lbl_mostrar_cand.pack()
            self.lbl_cadidato = tk.Label(self.candidato, text=f"{valor[0][1]}")
            self.lbl_cadidato.pack()

    def inserir_cadidato(self):
        nome = self.ent_nome.get()
        if nome == '':
            messagebox.showwarning('Aviso', 'Insira um nome!')
            self.ins_candidato.deiconify()
        else:
            if self.imagem == '':
                dir = os.path.dirname(__file__)
                self.imagem = f'{dir}/imgs/img1.png'
            sql = f'INSERT INTO candidato ("nome", "foto") VALUES("{nome}", "{self.imagem}");'
            bd.inserir(sql)
            messagebox.showinfo('Aviso', 'Candidato inserido com sucesso!')
            self.ent_nome.delete(0, 'end')
            self.ins_candidato.deiconify()

    def atualizar_tvw_candidato(self):
        for i in self.tvw.get_children():
            self.tvw.delete(i)
        query = 'SELECT id, nome FROM candidato;'
        dados = bd.consultar(query)
        for tupla in dados:
            self.tvw.insert('', tk.END, values=tupla)

    def pesquisar_tvw_candidato(self):
        busca = self.ent_pesq.get()
        for i in self.tvw.get_children():
            self.tvw.delete(i)
        if busca == '':
            self.atualizar_tvw_candidato()
        else:
            query = f"SELECT id, nome FROM candidato WHERE nome LIKE '{busca}';"
            dados = bd.consultar(query)
            for tupla in dados:
                self.tvw.insert('', tk.END, values=tupla)

    def atualizar_tvw_cargo(self):
        for i in self.tvw.get_children():
            self.tvw.delete(i)
        query = 'SELECT * FROM cargo;'
        dados = bd.consultar(query)
        for tupla in dados:
            self.tvw.insert('', tk.END, values=tupla)

    def pesquisar_tvw_cargo(self):
        busca = self.ent_pesq.get()
        for i in self.tvw.get_children():
            self.tvw.delete(i)
        if busca == '':
            self.atualizar_tvw_cargo()
        else:
            query = f"SELECT * FROM cargo WHERE nome LIKE '{busca}';"
            dados = bd.consultar(query)
            for tupla in dados:
                self.tvw.insert('', tk.END, values=tupla)

    def mostrar_cargo(self):
        self.cargo_mostrar = tk.Toplevel(self.janela)
        self.cargo_mostrar.geometry("900x500")
        self.cargo_mostrar.title("Cargos")
        self.lbl_cargo = tk.Label(self.cargo_mostrar, text="                 Cargos", font=32)
        self.lbl_cargo.pack()
        self.frm_pesq = tk.Frame(self.cargo_mostrar)
        self.frm_pesq.pack(fill=tk.BOTH, padx=90)
        self.lbl_pesq = tk.Label(self.frm_pesq, text="Pesquisar:")
        self.lbl_pesq.grid(column=0, row=0)
        self.ent_pesq = tk.Entry(self.frm_pesq)
        self.ent_pesq.grid(column=1, row=0)
        self.btn_pesq = tk.Button(self.frm_pesq, text="O", width=3, command=self.pesquisar_tvw_candidato)
        self.btn_pesq.grid(column=2, row=0, padx=3, pady=5)

        self.voltar = tk.Button(self.cargo_mostrar, text="Voltar", command=self.cargo_mostrar.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)
        self.tvw_cargos = ttk.Treeview(self.cargo_mostrar, columns=('Id', 'Nome do cargo', 'Candidato', 'Partido', 'Número','Eleição'), show='headings', height=18)
        self.tvw_cargos.column('Id', width=40)
        self.tvw_cargos.column('Nome do cargo', width=150)
        self.tvw_cargos.column('Candidato', width=150)
        self.tvw_cargos.column('Partido', width=150)
        self.tvw_cargos.column('Número', width=150)
        self.tvw_cargos.column('Eleição', width=150)
        self.tvw_cargos.heading('Id', text='Id')
        self.tvw_cargos.heading('Nome do cargo', text='Nome do Cargo')
        self.tvw_cargos.heading('Candidato', text='Candidato')
        self.tvw_cargos.heading('Partido', text='Partido')
        self.tvw_cargos.heading('Número', text='Número')
        self.tvw_cargos.heading('Eleição', text='Eleição')
        self.tvw_cargos.pack()
        #self.atualizar_tvw_cargo()

        self.frm_botao = tk.Frame(self.cargo_mostrar)
        self.frm_botao.pack(pady=10)

        self.btn_inserir = tk.Button(self.frm_botao, text="Adicionar", command=self.adicionar_cargo, width=8)
        self.btn_inserir.grid(column=0, row=0)
        self.btn_editar = tk.Button(self.frm_botao, text="Editar", command=self.editar_cargo,width=8)
        self.btn_editar.grid(column=1, row=0, padx=5)
        self.btn_excluir = tk.Button(self.frm_botao, text="Excluir", command=self.excluir_cargo,width=8)
        self.btn_excluir.grid(column=2, row=0)

    def adicionar_cargo(self):
        pass
    def editar_cargo(self):
        pass
    def excluir_cargo(self):
        pass

    def mostrar_eleicoes(self):
        self.eleicoes_mostrar = tk.Toplevel(self.janela)
        self.eleicoes_mostrar.geometry("900x500")
        self.eleicoes_mostrar.title("Eleições")
        self.voltar = tk.Button(self.eleicoes_mostrar, text="Voltar", command=self.eleicoes_mostrar.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)
        self.lbl_cargo = tk.Label(self.eleicoes_mostrar, text="     Eleições", font=32)
        self.lbl_cargo.pack()
        self.frm_pesq = tk.Frame(self.eleicoes_mostrar)
        self.frm_pesq.pack(fill=tk.BOTH, padx=20)
        self.lbl_pesq = tk.Label(self.frm_pesq, text="Pesquisar:")
        self.lbl_pesq.grid(column=0, row=0)
        self.ent_pesq = tk.Entry(self.frm_pesq)
        self.ent_pesq.grid(column=1, row=0)
        self.btn_pesq = tk.Button(self.frm_pesq, text="O", width=3, command=self.pesquisar_tvw_candidato)
        self.btn_pesq.grid(column=2, row=0, padx=3, pady=5)

        self.tvw_eleicao = ttk.Treeview(self.eleicoes_mostrar, columns=(
        'Id', 'Nome da eleição', 'Descrição', 'Candidatos', 'Inicio', 'Fim', 'Ativo'), show='headings', height=18)
        self.tvw_eleicao.column('Id', width=40)
        self.tvw_eleicao.column('Nome da eleição', width=150)
        self.tvw_eleicao.column('Descrição', width=150)
        self.tvw_eleicao.column('Candidatos', width=150)
        self.tvw_eleicao.column('Inicio', width=100)
        self.tvw_eleicao.column('Fim', width=100)
        self.tvw_eleicao.column('Ativo', width=100)
        self.tvw_eleicao.heading('Id', text='Id')
        self.tvw_eleicao.heading('Nome da eleição', text='Nome da eleição')
        self.tvw_eleicao.heading('Descrição', text='Descrição')
        self.tvw_eleicao.heading('Candidatos', text='Candidatos')
        self.tvw_eleicao.heading('Inicio', text='Inicio')
        self.tvw_eleicao.heading('Fim', text='Fim')
        self.tvw_eleicao.heading('Ativo', text='Ativo')
        self.tvw_eleicao.pack()

        self.frm_botao = tk.Frame(self.eleicoes_mostrar)
        self.frm_botao.pack(pady=10)

        self.btn_inserir = tk.Button(self.frm_botao, text="Adicionar", command=self.adicionar_cargo, width=8)
        self.btn_inserir.grid(column=0, row=0)
        self.btn_editar = tk.Button(self.frm_botao, text="Editar", command=self.editar_cargo, width=8)
        self.btn_editar.grid(column=1, row=0, padx=5)
        self.btn_excluir = tk.Button(self.frm_botao, text="Excluir", command=self.excluir_cargo, width=8)
        self.btn_excluir.grid(column=2, row=0)

    def atualizar_tvw_eleicao(self):
        for i in self.tvw.get_children():
            self.tvw.delete(i)
        query = 'SELECT * FROM eleicao;'
        dados = bd.consultar(query)
        for tupla in dados:
            self.tvw.insert('', tk.END, values=tupla)

    def pesquisar_tvw_eleicao(self):
        busca = self.ent_pesq.get()
        for i in self.tvw.get_children():
            self.tvw.delete(i)
        if busca == '':
            self.atualizar_tvw_eleicao()
        else:
            query = f"SELECT * FROM cargo WHERE nome LIKE '{busca}';"
            dados = bd.consultar(query)
            for tupla in dados:
                self.tvw.insert('', tk.END, values=tupla)

    def login(self):
        self.login = tk.Toplevel()
        self.login.geometry("400x400")
        self.login.title("Login")
        # Login/Cadastro
        self.frm_login = tk.Frame(self.login)
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

        self.btn_login = tk.Button(self.frm_login, text="Entrar", command=self.confirma_login, width=12)
        self.btn_login.grid(column=0, row=6, columnspan=1)

        self.btn_cadastro = tk.Button(self.frm_login, text="Cadastre-se", command=self.cadastro, width=12)
        self.btn_cadastro.grid(column=0, row=7, pady=20)

        self.btn_destroir = tk.Button(self.frm_login, text="VOTE AQUI", command=self.votacao)
        self.btn_destroir.grid(column=1, row=7)

        self.btn_admin = tk.Button(self.frm_login, text="ADMINISTRADOR", command=self.adm)
        self.btn_admin.grid(column=1, row=8)

    def adm(self):
        self.login.destroy()
        self.janela.deiconify()

    # Funções
    def confirma_login(self):
        cpf = self.ent_cpf.get()
        senha = self.ent_senha.get().encode("utf-8")
        if cpf == "":
            messagebox.showinfo("Insira o cpf", "O campo cpf está vazio!")
        elif senha == "":
            messagebox.showinfo("Insira a senha", "O campo senha está vazio!")
        else:
            query = 'SELECT cpf, senha, id FROM usuario;'
            valores = bd.consultar(query)
            logado = False
            for i in valores:
                if i[0] == cpf:
                    hash = i[1][2:len(i[1])-1].encode("utf-8")
                    if bcrypt.checkpw(senha, hash):
                        logado = True
                        self.user_logged = i[2]
            if logado:
                if self.user_logged == 0:
                    self.login.destroy()
                    self.janela.deiconify()
                else:
                    self.votacao()
                    self.login.destroy()
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

    def votacao(self):
        self.votar = tk.Toplevel(self.janela)
        self.votar.geometry("800x600")
        self.votar.title("Área de votos")


app = tk.Tk()
Tela(app)
app.mainloop()
