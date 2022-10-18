import tkinter as tk
from tkinter import messagebox, ttk, Menu
from tkinter import filedialog as fd
import banco_de_dados as bd
import bcrypt
import os
from PIL import Image
from tkcalendar import DateEntry
import re

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
        #self.cand_menu.add_command(label="Adicionar candidato", command=self.inserir_candidatos)
        self.cand_menu.add_command(label="Mostrar candidatos", command=self.candidatos)
        self.menu_bar.add_cascade(label="Candidatos", menu=self.cand_menu)

        self.cargo_menu = Menu(self.menu_bar, tearoff=0)
        #self.cargo_menu.add_command(label="Adicionar cargos", command=self.inserir_cargo)
        self.cargo_menu.add_command(label="Mostrar cargos", command=self.mostrar_cargo)
        self.menu_bar.add_cascade(label="Cargos", menu=self.cargo_menu)

        self.eleicao_menu = Menu(self.menu_bar, tearoff=0)
        #self.eleicao_menu.add_command(label="Adicionar eleições", command=self.inserir_eleicao)
        self.eleicao_menu.add_command(label="Mostrar eleições", command=self.mostrar_eleicoes)
        self.menu_bar.add_cascade(label="Eleições", menu=self.eleicao_menu)

        self.config_menu = Menu(self.menu_bar, tearoff=0)
        self.config_menu.add_command(label="Login", command=self.login)
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
        #, relwidth=0.50, relheight=0.85
        self.frm_pesq = tk.Frame(self.candidatos)
        self.frm_pesq.pack()
        self.lbl_pesq = tk.Label(self.frm_pesq, text="Pesquisar:")
        self.lbl_pesq.grid(column=0, row=0)
        self.ent_pesq = tk.Entry(self.frm_pesq)
        self.ent_pesq.grid(column=1, row=0)

        self.minha_imagem = tk.PhotoImage(file="imgs/lupa.png")

        self.btn_pesq = tk.Button(self.frm_pesq, text="O", image=self.minha_imagem, width=16, command=self.pesquisar_tvw_candidato)
        self.btn_pesq.grid(column=2, row=0, padx=3, pady=5)

        self.imagem_refresh = tk.PhotoImage(file="imgs/refresh.png")
        self.btn_refresh = tk.Button(self.frm_pesq, image=self.imagem_refresh, width=16, command=self.refresh_tvw_candidato)
        self.btn_refresh.grid(column=3, row=0, padx=3)

        self.voltar = tk.Button(self.candidatos, text="Voltar", command=self.candidatos.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)

        self.tvw_candidato = ttk.Treeview(self.candidatos, columns=('id', 'nome'), show='headings')
        self.tvw_candidato.column('id', width=40)
        self.tvw_candidato.column('nome', width=250)
        self.tvw_candidato.heading('id', text='Id')
        self.tvw_candidato.heading('nome', text='Nome')
        self.tvw_candidato.pack()
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

    def refresh_tvw_candidato(self):
        for i in self.tvw_candidato.get_children():
            self.tvw_candidato.delete(i)
        query = f"SELECT id, nome FROM candidato;"
        dados = bd.consultar(query)
        for tupla in dados:
            self.tvw_candidato.insert('', tk.END, values=tupla)
    def editar_candidato(self):
        selecionado = self.tvw_candidato.selection()
        lista = self.tvw_candidato.item(selecionado, "values")

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
        selecionado = self.tvw_candidato.selection()
        lista = self.tvw_candidato.item(selecionado, "values")
        nome = self.ent_nome.get()
        if nome == "":
            messagebox.showinfo("O campo nome está vazio!")
        else:
            mensagem = messagebox.askyesno("CUIDADO", "Você tem certeza que deseja realizar a(s) alteração(ões)?")
            if mensagem:
                if self.nova_img == '':
                    query = f'UPDATE candidato SET nome="{nome}" WHERE id={lista[0]};'
                    bd.atualizar(query)
                    self.atualizar_tvw_candidato()
                    self.edit_cand.destroy()
                    self.candidatos.deiconify()
                else:
                    query = f'UPDATE candidato SET nome="{nome}", foto="{self.nova_img}" WHERE id={lista[0]};'
                    bd.atualizar(query)
                    self.atualizar_tvw_candidato()
                    self.edit_cand.destroy()
                    self.candidatos.deiconify()
            else:
                self.edit_cand.destroy()
                self.candidatos.deiconify()

    def excluir_candidato(self):
        selecionado = self.tvw_candidato.selection()
        lista = self.tvw_candidato.item(selecionado, "values")
        mensagem = messagebox.askyesno("Excluir", "Você tem certeza que deseja excluir o candidato?")
        if mensagem:
            sql = f'DELETE FROM candidato WHERE id={lista[0]};'
            bd.deletar(sql)
            messagebox.showinfo("Excluído", "Candidato excluído com sucesso")
            self.atualizar_tvw_candidato()
        self.candidatos.deiconify()

    def imagem_candidato(self):
        tipos = (('Imagem', '*.PNG'), ('Imagem', '*.JPG'), ('Todos', '*.*'))
        self.imagem = fd.askopenfilename(initialdir=f'/imgs', filetypes=tipos)
        if self.imagem.endswith(".jpg"):
            img = Image.open(f'{self.imagem}')
            self.imagem = self.imagem.replace(".jpg", "")
            img.resize((150, 150), Image.ANTIALIAS)
            img.save(f'{self.imagem}.png')
            os.remove(f'{self.imagem}.jpg')
            self.imagem = f"{self.imagem}.png"
        else:
            img = Image.open(f'{self.imagem}')
            img = img.resize((150, 150), Image.ANTIALIAS)
            img.save(f'{self.imagem}')
            self.imagem = f"{self.imagem}"
        self.ins_candidato.deiconify()

    def mostrar_candidato(self):
        selecionado = self.tvw_candidato.selection()
        if selecionado == ():
            messagebox.showinfo("Selecine candidato", "Selecione um candidato")
            self.candidatos.deiconify()
        else:
            self.candidato = tk.Toplevel(self.janela)
            self.candidato.title("Candidato")
            id = self.tvw_candidato.item(selecionado, 'values')[0]
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
            self.atualizar_tvw_candidato()
            messagebox.showinfo('Aviso', 'Candidato inserido com sucesso!')
            self.ins_candidato.deiconify()

    def atualizar_tvw_candidato(self):
        for i in self.tvw_candidato.get_children():
            self.tvw_candidato.delete(i)
        query = 'SELECT id, nome FROM candidato;'
        dados = bd.consultar(query)
        for tupla in dados:
            self.tvw_candidato.insert('', tk.END, values=tupla)

    def pesquisar_tvw_candidato(self):
        busca = self.ent_pesq.get()
        for i in self.tvw_candidato.get_children():
            self.tvw_candidato.delete(i)
        if busca == '':
            self.atualizar_tvw_candidato()
        else:
            query = f"SELECT id, nome FROM candidato WHERE nome LIKE '{busca}%';"
            dados = bd.consultar(query)
            for tupla in dados:
                self.tvw_candidato.insert('', tk.END, values=tupla)

    def atualizar_tvw_cargo(self):
        for i in self.tvw_cargos.get_children():
            self.tvw_cargos.delete(i)
        query = 'SELECT cargo_id, nome_cargo, candidato_id, nome_candidato, partido, num_candidato FROM cargo;'
        dados = bd.consultar(query)

        for tupla in dados:
            self.tvw_cargos.insert('', tk.END, values=tupla)

    def pesquisar_tvw_cargo(self):
        busca = self.ent_pesq.get()
        for i in self.tvw_cargos.get_children():
            self.tvw_cargos.delete(i)
        if busca == '':
            self.atualizar_tvw_cargo()
        else:
            query = f"SELECT cargo_id, nome_cargo, candidato_id, nome, partido, num_candidato FROM cargo, candidato WHERE candidato_id = id AND nome LIKE '{busca}%';"
            dados = bd.consultar(query)
            for tupla in dados:
                self.tvw_cargos.insert('', tk.END, values=tupla)

    def filtrar_tvw_cargo(self):
        busca = self.cbx_filtro.get()
        for i in self.tvw_cargos.get_children():
            self.tvw_cargos.delete(i)
        if busca == '':
            self.atualizar_tvw_cargo()
        else:
            if busca != "Todos":
                query = f"SELECT cargo_id, nome_cargo, candidato_id, nome, partido, num_candidato FROM cargo, candidato WHERE candidato_id = id AND nome_cargo LIKE '{busca}%';"
                dados = bd.consultar(query)
                for tupla in dados:
                    self.tvw_cargos.insert('', tk.END, values=tupla)
            else:
                query = f"SELECT cargo_id, candidato_id, nome_cargo, nome, partido, num_candidato FROM cargo, candidato WHERE candidato_id = id;"
                dados = bd.consultar(query)
                for tupla in dados:
                    self.tvw_cargos.insert('', tk.END, values=tupla)

    def refresh_tvw_cargos(self):
        for i in self.tvw_cargos.get_children():
            self.tvw_cargos.delete(i)
        query = f"SELECT cargo_id, nome_cargo, candidato_id, nome, partido, num_candidato FROM cargo, candidato WHERE candidato_id = id AND nome_cargo LIKE '{busca}%';"
        dados = bd.consultar(query)
        for tupla in dados:
            self.tvw_candidato.insert('', tk.END, values=tupla)

    def mostrar_cargo(self):
        self.cargo_mostrar = tk.Toplevel(self.janela)
        self.cargo_mostrar.geometry("750x500")
        self.cargo_mostrar.title("Cargos")
        self.lbl_cargo = tk.Label(self.cargo_mostrar, text="                 Cargos", font=32)
        self.lbl_cargo.pack()

        self.frm_pesq = tk.Frame(self.cargo_mostrar)
        self.frm_pesq.pack(fill=tk.BOTH, padx=85)
        self.lbl_filtro = tk.Label(self.frm_pesq, text="Filtro:")
        self.lbl_filtro.grid(column=1, row=0)
        self.cbx_filtro = ttk.Combobox(self.frm_pesq)
        query = 'SELECT DISTINCT nome_cargo FROM cargo;'
        valores = bd.consultar_cargos(query)
        self.cbx_filtro['values'] = (f'"Todos" {valores}')
        self.cbx_filtro.grid(column=2, row=0)
        self.cbx_filtro.current(0)

        self.minha_imagem = tk.PhotoImage(file="imgs/lupa.png")
        self.btn_filtro = tk.Button(self.frm_pesq, width=15, command=self.filtrar_tvw_cargo, image=self.minha_imagem)
        self.btn_filtro.grid(column=3, row=0, padx=2, pady=5)


        self.lbl_pesq = tk.Label(self.frm_pesq, text="Pesquisar:")
        self.lbl_pesq.grid(column=4, row=0, padx=5)
        self.ent_pesq = tk.Entry(self.frm_pesq)
        self.ent_pesq.grid(column=5, row=0)

        self.btn_pesq = tk.Button(self.frm_pesq, image=self.minha_imagem, width=16, command=self.pesquisar_tvw_cargo)
        self.btn_pesq.grid(column=6, row=0, padx=3, pady=5)

        self.imagem_refresh = tk.PhotoImage(file="imgs/refresh.png")
        self.btn_refresh = tk.Button(self.frm_pesq, image=self.imagem_refresh, width=16,
                                     command=self.refresh_tvw_cargos)
        self.btn_refresh.grid(column=7, row=0, padx=3)

        self.voltar = tk.Button(self.cargo_mostrar, text="Voltar", command=self.cargo_mostrar.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)
        self.tvw_cargos = ttk.Treeview(self.cargo_mostrar, columns=('Id', 'Nome do cargo', "Id candidato", 'Candidato', 'Partido', 'Número'), show='headings', height=18)
        self.tvw_cargos.column('Id', width=40)
        self.tvw_cargos.column('Nome do cargo', width=120)
        self.tvw_cargos.column('Id candidato', width=75)
        self.tvw_cargos.column('Candidato', width=180)
        self.tvw_cargos.column('Partido', width=110)
        self.tvw_cargos.column('Número', width=110)
        self.tvw_cargos.heading('Id', text='Id')
        self.tvw_cargos.heading('Nome do cargo', text='Nome do Cargo')
        self.tvw_cargos.heading('Id candidato', text='Id candidato')
        self.tvw_cargos.heading('Candidato', text='Candidato')
        self.tvw_cargos.heading('Partido', text='Partido')
        self.tvw_cargos.heading('Número', text='Número')
        self.tvw_cargos.pack()
        self.atualizar_tvw_cargo()

        self.frm_botao = tk.Frame(self.cargo_mostrar)
        self.frm_botao.pack(pady=10)

        self.btn_inserir = tk.Button(self.frm_botao, text="Adicionar", command=self.inserir_cargo, width=8)
        self.btn_inserir.grid(column=0, row=0)
        self.btn_editar = tk.Button(self.frm_botao, text="Editar", command=self.editar_cargo,width=8)
        self.btn_editar.grid(column=1, row=0, padx=5)
        self.btn_excluir = tk.Button(self.frm_botao, text="Excluir", command=self.excluir_cargo,width=8)
        self.btn_excluir.grid(column=2, row=0)

    def inserir_cargo(self):
        self.ins_cargo = tk.Toplevel(self.janela)
        self.ins_cargo.title("Inserir cargos")
        self.ins_cargo.geometry("480x410")
        self.voltar = tk.Button(self.ins_cargo, text="Voltar", command=self.ins_cargo.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)
        self.lbl_titulo = tk.Label(self.ins_cargo, text="Cadastrar cargos", font=32)
        self.lbl_titulo.pack()

        self.frmpesq = tk.Frame(self.ins_cargo)
        self.frmpesq.pack(fill=tk.BOTH, padx=59)
        self.lbl_pesq = tk.Label(self.frmpesq, text="Pesquisar:")
        self.lbl_pesq.grid(column=0, row=0)
        self.ent_pesq = tk.Entry(self.frmpesq)
        self.ent_pesq.grid(column=1, row=0)
        self.minha_imagem = tk.PhotoImage(file="imgs/lupa.png")
        self.btn_pesq = tk.Button(self.frm_pesq, text="O", image=self.minha_imagem, width=16, command=self.pesquisar_tvw_candidatos_cargos)
        self.btn_pesq.grid(column=2, row=0, padx=3, pady=5)

        self.tvw_candidato = ttk.Treeview(self.ins_cargo, columns=('id', 'nome'), show='headings', height=5)
        self.tvw_candidato.column('id', width=40)
        self.tvw_candidato.column('nome', width=250)
        self.tvw_candidato.heading('id', text='Id')
        self.tvw_candidato.heading('nome', text='Nome')
        self.tvw_candidato.pack()
        self.atualizar_tvw_candidato()

        self.btn_nome_candidato = tk.Button(self.ins_cargo, text="Selecionar candidato", command=self.selecionar_candidato)
        self.btn_nome_candidato.pack(pady=5)
        self.candidato_selecionado = ''

        self.frm_cargo = tk.Frame(self.ins_cargo)
        self.frm_cargo.pack(fill=tk.BOTH, padx=20)

        self.lbl_nome_candidato = tk.Label(self.frm_cargo, text='Nome do candidato:')
        self.lbl_nome_candidato.grid(column=0, row=2, pady=7)
        self.ent_nome_candidato = tk.Entry(self.frm_cargo)
        self.ent_nome_candidato.grid(column=1, row=2)

        self.lbl_nome = tk.Label(self.frm_cargo, text='Nome do cargo:')
        self.lbl_nome.grid(column=0, row=3, pady=7)
        self.ent_nome = tk.Entry(self.frm_cargo)
        self.ent_nome.grid(column=1, row=3)

        self.lbl_partido = tk.Label(self.frm_cargo, text="Nome do partido:")
        self.lbl_partido.grid(column=0, row=4, pady=7)
        self.ent_partido = tk.Entry(self.frm_cargo)
        self.ent_partido.grid(column=1, row=4)

        self.lbl_num_cand = tk.Label(self.frm_cargo, text="Número do candidato:")
        self.lbl_num_cand.grid(column=0, row=5, pady=7)
        self.ent_num_cand = tk.Entry(self.frm_cargo)
        self.ent_num_cand.grid(column=1, row=5)

        self.btn_conf_cargo = tk.Button(self.frm_cargo, text="Confirmar", command=self.confirmar_add_cargo)
        self.btn_conf_cargo.grid(column=1, row=6, columnspan=2, pady=7)

    def selecionar_candidato(self):
        selecionado = self.tvw_candidato.selection()
        lista = self.tvw_candidato.item(selecionado, "values")
        self.ent_nome_candidato.delete(0, tk.END)
        self.ent_nome_candidato.insert(0, lista[1])
        self.candidato_selecionado = lista[0]

    def confirmar_add_cargo(self):
        nome = self.ent_nome.get()
        partido = self.ent_partido.get()
        numero = self.ent_num_cand.get()
        candidato = self.candidato_selecionado
        if nome == '':
            messagebox.showwarning('Aviso', 'Insira o nome do cargo!')
            self.ins_cargo.deiconify()
        elif partido == '':
            messagebox.showwarning('Aviso', 'Insira o nome do partido!')
            self.ins_cargo.deiconify()
        elif numero == '':
            messagebox.showwarning('Aviso', 'Insira o numero do candidato!')
            self.ins_cargo.deiconify()
        elif candidato == '':
            messagebox.showwarning('Aviso', 'Selecione um candidato! Não esqueça de clicar em "Selecionar Candidato"')
            self.ins_cargo.deiconify()
        else:
            sql = f'SELECT num_candidato FROM cargo'
            valores = bd.consultar(sql)
            igual = False
            for i in valores:
                if str(i) == f"({numero},)":
                    igual = True
            if igual:
                messagebox.showwarning('Aviso', 'Número de candidato existente, por favor insira um outro número!')
                self.ins_cargo.deiconify()
            else:
                query = f'SELECT nome FROM candidato WHERE id = {candidato};'
                nome_candidato = bd.consultar_cargos(query)
                print(nome_candidato)
                query = f'INSERT INTO cargo ("candidato_id", "nome_candidato", "nome_cargo", "partido", "num_candidato") VALUES ("{candidato}", "{nome_candidato}", "{nome}", "{partido}", "{numero}");'
                bd.inserir(query)
                self.atualizar_tvw_cargo()
                messagebox.showinfo("Aviso", "Cargo inserido com sucesso!")
                query = 'SELECT DISTINCT nome_cargo FROM cargo;'
                valores = bd.consultar_cargos(query)
                self.cbx_filtro['values'] = (f'"Todos" {valores}')
                self.ins_cargo.destroy()
                self.cargo_mostrar.deiconify()

    def editar_cargo(self):
        selecionado = self.tvw_cargos.selection()
        lista = self.tvw_cargos.item(selecionado, "values")

        self.edit_cargo = tk.Toplevel()
        self.edit_cargo.title("Editar candidato")
        self.edit_cargo.geometry("430x410")
        self.edit_cargo.resizable(False,False)
        self.voltar = tk.Button(self.edit_cargo, text="Voltar", command=self.edit_cargo.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)

        self.nome = tk.Label(self.edit_cargo, text="Editar candidato", font=32)
        self.nome.pack()

        self.frmpesq = tk.Frame(self.edit_cargo)
        self.frmpesq.pack(fill=tk.BOTH, padx=34)
        self.lbl_pesq = tk.Label(self.frmpesq, text="Pesquisar:", command=self.pesquisar_tvw_candidatos_cargos)
        self.lbl_pesq.grid(column=0, row=0)
        self.ent_pesq = tk.Entry(self.frmpesq)
        self.ent_pesq.grid(column=1, row=0)
        self.minha_imagem = tk.PhotoImage(file="imgs/lupa.png")
        self.btn_pesq = tk.Button(self.frm_pesq, text="O", image=self.minha_imagem, width=16)
        self.btn_pesq.grid(column=2, row=0, padx=3, pady=5)


        self.tvw_candidato = ttk.Treeview(self.edit_cargo, columns=('id', 'nome'), show='headings', height=5)
        self.tvw_candidato.column('id', width=40)
        self.tvw_candidato.column('nome', width=250)
        self.tvw_candidato.heading('id', text='Id')
        self.tvw_candidato.heading('nome', text='Nome')
        self.tvw_candidato.pack()
        self.atualizar_tvw_candidato()

        self.btn_nome_candidato = tk.Button(self.edit_cargo, text="Selecionar candidato",
                                            command=self.selecionar_edit_candidato)
        self.btn_nome_candidato.pack(pady=7)
        self.candidato_selecionado = ''

        self.frm_edit = tk.Frame(self.edit_cargo)
        self.frm_edit.pack()
        self.lbl_nome_candidato = tk.Label(self.frm_edit, text="Nome do candidato:")
        self.lbl_nome_candidato.grid(column=0, row=0, pady=7)
        self.ent_nome_candidato = tk.Entry(self.frm_edit, width=30)
        self.ent_nome_candidato.grid(column=1, row=0)
        self.ent_nome_candidato.insert(0, lista[3])

        self.ent_id_candidato = tk.Entry(self.edit_cargo)
        self.ent_id_candidato.insert(0, lista[2])

        self.lbl_nome_cargo = tk.Label(self.frm_edit, text="Nome do cargo:")
        self.lbl_nome_cargo.grid(column=0, row=1, pady=7)
        self.ent_nome_cargo = tk.Entry(self.frm_edit, width=30)
        self.ent_nome_cargo.grid(column=1, row=1)
        self.ent_nome_cargo.insert(0, lista[1])

        self.lbl_partido = tk.Label(self.frm_edit, text="Partido:")
        self.lbl_partido.grid(column=0, row=2, pady=7)
        self.ent_partido = tk.Entry(self.frm_edit, width=30)
        self.ent_partido.grid(column=1, row=2)
        self.ent_partido.insert(0, lista[4])

        self.lbl_num_cand = tk.Label(self.frm_edit, text="Número do candidato:")
        self.lbl_num_cand.grid(column=0, row=3, pady=7)
        self.ent_num_cand = tk.Entry(self.frm_edit, width=30)
        self.ent_num_cand.grid(column=1, row=3)
        self.ent_num_cand.insert(0, lista[5])

        self.btn_cof_edit_cargo = tk.Button(self.frm_edit, text="Confirmar", command= self.confirma_editar_cargo)
        self.btn_cof_edit_cargo.grid(column=0, row=4, columnspan=2, pady=7)

    def selecionar_edit_candidato(self):
        self.ent_nome_candidato.delete(0, tk.END)
        selecionado = self.tvw_candidato.selection()
        lista = self.tvw_candidato.item(selecionado, "values")
        self.ent_nome_candidato.insert(0, lista[1])
        self.ent_id_candidato.delete(0, tk.END)
        self.ent_id_candidato.insert(0, lista[0])

    def confirma_editar_cargo(self):
        selecionado = self.tvw_cargos.selection()
        lista = self.tvw_cargos.item(selecionado, "values")
        candidato = self.ent_nome_candidato.get()
        cargo = self.ent_nome_cargo.get()
        partido = self.ent_partido.get()
        numero = self.ent_num_cand.get()

        if lista[1] == cargo and lista[2] == candidato and lista[3] == partido and lista[4] == numero:
            message = messagebox.askyesno("Sem alterações", "Você tem certeza que não deseja realizar nenhuma alteração?")
            if message:
                self.edit_cargo.destroy()
                self.cargo_mostrar.deiconify()
            else:
                self.edit_cargo.deiconify()
        else:
            message = messagebox.askyesno("Alterações realizadas", "Você tem certeza que deseja realizar as alterações?")
            if message:
                query = f'UPDATE cargo SET candidato_id="{self.ent_id_candidato.get()}", nome_candidato="{candidato}", nome_cargo="{cargo}", partido="{partido}", num_candidato={numero} WHERE cargo_id={lista[0]};'
                bd.atualizar(query)
                self.atualizar_tvw_cargo()
                self.edit_cargo.destroy()
                self.cargo_mostrar.deiconify()
            else:
                self.edit_eleicao.deiconify()

    def excluir_cargo(self):
        selecionado = self.tvw_cargos.selection()
        lista = self.tvw_cargos.item(selecionado, "values")
        if selecionado != ():
            mensagem = messagebox.askyesno("Excluir", "Você tem certeza que deseja excluir o cargo selecionado?")
            if mensagem:
                sql = f'DELETE FROM cargo WHERE cargo_id={lista[0]};'
                bd.deletar(sql)
                self.atualizar_tvw_cargo()
                messagebox.showinfo("Excluído", "Cargo excluído com sucesso!")
            self.cargo_mostrar.deiconify()

    def mostrar_eleicoes(self):
        self.eleicoes_mostrar = tk.Toplevel(self.janela)
        self.eleicoes_mostrar.geometry("1100x500")
        self.eleicoes_mostrar.title("Eleições")
        self.voltar = tk.Button(self.eleicoes_mostrar, text="Voltar", command=self.eleicoes_mostrar.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)
        self.lbl_cargo = tk.Label(self.eleicoes_mostrar, text="     Eleições", font=32)
        self.lbl_cargo.pack()
        self.frm_pesq = tk.Frame(self.eleicoes_mostrar)
        self.frm_pesq.pack(fill=tk.BOTH, padx=38)
        self.lbl_pesq = tk.Label(self.frm_pesq, text="Pesquisar:")
        self.lbl_pesq.grid(column=0, row=0)
        self.ent_pesq = tk.Entry(self.frm_pesq)
        self.ent_pesq.grid(column=1, row=0)
        self.minha_imagem = tk.PhotoImage(file="imgs/lupa.png")
        self.btn_pesq = tk.Button(self.frm_pesq, text="O", image=self.minha_imagem, width=16, command=self.pesquisar_tvw_eleicao)
        self.btn_pesq.grid(column=2, row=0, padx=3, pady=5)

        self.tvw_eleicao = ttk.Treeview(self.eleicoes_mostrar, columns=(
        'Id', 'Nome da eleição', 'Descrição', 'Cargo', 'Inicio', 'Fim', "Candidatos" ,'Status'), show='headings', height=18)
        self.tvw_eleicao.column('Id', width=40)
        self.tvw_eleicao.column('Nome da eleição', width=200)
        self.tvw_eleicao.column('Descrição', width=200)
        self.tvw_eleicao.column('Cargo', width=110)
        self.tvw_eleicao.column('Inicio', width=75)
        self.tvw_eleicao.column('Fim', width=75)
        self.tvw_eleicao.column('Candidatos', width=200)
        self.tvw_eleicao.column('Status', width=50)
        self.tvw_eleicao.heading('Id', text='Id')
        self.tvw_eleicao.heading('Nome da eleição', text='Nome da eleição')
        self.tvw_eleicao.heading('Descrição', text='Descrição')
        self.tvw_eleicao.heading('Cargo', text='Cargo')
        self.tvw_eleicao.heading('Inicio', text='Inicio')
        self.tvw_eleicao.heading('Fim', text='Fim')
        self.tvw_eleicao.heading('Candidatos', text='Candidatos')
        self.tvw_eleicao.heading('Status', text='Status')
        self.tvw_eleicao.pack()

        self.atualizar_tvw_eleicao()

        self.frm_botao = tk.Frame(self.eleicoes_mostrar)
        self.frm_botao.pack(pady=10)

        self.btn_inserir = tk.Button(self.frm_botao, text="Cadastrar", command=self.inserir_eleicao, width=8)
        self.btn_inserir.grid(column=0, row=0, padx=3)
        self.btn_editar = tk.Button(self.frm_botao, text="Editar", command=self.editar_eleicao, width=8)
        self.btn_editar.grid(column=1, row=0, padx=3)
        self.btn_excluir = tk.Button(self.frm_botao, text="Excluir", command=self.excluir_eleicao, width=8)
        self.btn_excluir.grid(column=2, row=0, padx=3)
        self.btn_add_cand = tk.Button(self.frm_botao, text="Adicionar candidatos", command=self.adicionar_candidatos)
        self.btn_add_cand.grid(column=4, row=0, padx=3)
        self.btn_add_cand = tk.Button(self.frm_botao, text="Encerrar eleição", command=self.encerrar_eleicao)
        self.btn_add_cand.grid(column=3, row=0, padx=3)

    def adicionar_candidatos(self):
        selecionado = self.tvw_eleicao.selection()
        lista = self.tvw_eleicao.item(selecionado, "values")
        if selecionado != ():
            self.add_candidatos = tk.Toplevel()
            self.add_candidatos.geometry("400x330")
            self.voltar = tk.Button(self.add_candidatos, text="Voltar", command=self.add_candidatos.destroy, width=8)
            self.voltar.pack(side=tk.LEFT)

            self.frm_pesq = tk.Frame(self.add_candidatos)
            self.frm_pesq.pack(fill=tk.BOTH, padx=30)
            self.lbl_pesq = tk.Label(self.frm_pesq, text="Pesquisar:")
            self.lbl_pesq.grid(column=0, row=0)
            self.ent_pesq = tk.Entry(self.frm_pesq)
            self.ent_pesq.grid(column=1, row=0)
            self.minha_imagem = tk.PhotoImage(file="imgs/lupa.png")
            self.btn_pesq = tk.Button(self.frm_pesq, image=self.minha_imagem, width=16, command=self.pesquisar_tvw_candidatos_cargos)
            self.btn_pesq.grid(column=2, row=0, padx=3, pady=5)

            self.tvw_candidato = ttk.Treeview(self.add_candidatos, columns=('id', 'nome'), show='headings')
            self.tvw_candidato.column('id', width=40)
            self.tvw_candidato.column('nome', width=250)
            self.tvw_candidato.heading('id', text='Id')
            self.tvw_candidato.heading('nome', text='Nome')
            self.tvw_candidato.pack()
            self.atualizar_tvw_candidatos_cargos()

            self.btn_adc_cand = tk.Button(self.add_candidatos, text="Adicionar", command=self.confirmar_add_candidato)
            self.btn_adc_cand.pack(pady=10)

    def pesquisar_tvw_candidatos_cargos(self):
        selecionado = self.tvw_eleicao.selection()
        lista = self.tvw_eleicao.item(selecionado, "values")
        busca = self.ent_pesq.get()
        for i in self.tvw_candidato.get_children():
            self.tvw_candidato.delete(i)
        if busca == '':
            self.atualizar_tvw_candidatos_cargos()
        else:
            query = f"SELECT DISTINCT id, nome FROM candidato, cargo WHERE cargo.nome_cargo LIKE '{lista[3]}' AND candidato.id = cargo.candidato_id AND nome LIKE '{busca}%';"
            dados = bd.consultar(query)
            for tupla in dados:
                self.tvw_candidato.insert('', tk.END, values=tupla)

    def atualizar_tvw_candidatos_cargos(self):
        selecionado = self.tvw_eleicao.selection()
        lista = self.tvw_eleicao.item(selecionado, "values")
        for i in self.tvw_candidato.get_children():
            self.tvw_candidato.delete(i)
        query = f'SELECT id, nome FROM candidato, cargo WHERE cargo.nome_cargo LIKE "{lista[3]}" AND candidato.id = cargo.candidato_id;'
        dados = bd.consultar(query)
        for tupla in dados:
            self.tvw_candidato.insert('', tk.END, values=tupla)

    def confirmar_add_candidato(self):
        selecionado = self.tvw_candidato.selection()
        lista = self.tvw_candidato.item(selecionado, "values")
        eleicao = self.tvw_eleicao.selection()
        lista_eleicao = self.tvw_eleicao.item(eleicao, "values")
        if selecionado != ():
            message = messagebox.askyesno("Adicionar candidato", f'Você deseja adicionar o(a) "{lista[1]}" na eleicao "{lista_eleicao[1]}"')
            if message:
                sql = f'SELECT candidatos FROM eleicao WHERE eleicao_id = {lista_eleicao[0]};'
                tupla = bd.consultar_candidatos(sql)
                list = []
                if str(tupla) == "[(None,)]":
                    tupla.pop()
                else:
                    list.append(tupla)
                    num = ''
                    for i in list:
                        for j in i:
                            if j.isdigit():
                                num= num + j
                            else:
                                num = ''
                            if num == str(lista[0]):
                                message = messagebox.showinfo("Já cadastrado", "Candidato já cadastrado nesta eleição!")
                                break
                if message == "ok":
                    self.add_candidatos.deiconify()
                else:
                    list.append(lista)
                    query = f'UPDATE eleicao SET candidatos="{list}" WHERE eleicao_id={lista_eleicao[0]};'
                    bd.atualizar(query)
                    self.atualizar_tvw_eleicao()
                    self.add_candidatos.destroy()
                    self.eleicoes_mostrar.deiconify()
            else:
                self.add_candidatos.deiconify()

    def encerrar_eleicao(self):
        selecionado = self.tvw_eleicao.selection()
        lista = self.tvw_eleicao.item(selecionado, "values")

        if lista != ():
            message = messagebox.askyesno("Encerrar eleição", "Você tem certeza que deseja encerrar a eleição?")
            if message:
                query = f'UPDATE eleicao SET ativo=FALSE WHERE eleicao_id = {lista[0]};'
                bd.atualizar(query)
                self.atualizar_tvw_eleicao()
            self.eleicoes_mostrar.deiconify()

    def inserir_eleicao(self):
        self.ins_eleicao = tk.Toplevel(self.janela)
        self.ins_eleicao.title("Inserir eleições")
        self.ins_eleicao.geometry("400x300")
        self.voltar = tk.Button(self.ins_eleicao, text="Voltar", command=self.ins_eleicao.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)
        self.lbl_titulo = tk.Label(self.ins_eleicao, text="Cadastrar Eleição", font=32)
        self.lbl_titulo.pack()

        self.frm_eleicao = tk.Frame(self.ins_eleicao)
        self.frm_eleicao.pack()

        self.lbl_nome = tk.Label(self.frm_eleicao, text='Nome da eleição:')
        self.lbl_nome.grid(column=0, row=0, pady=10)
        self.ent_nome = tk.Entry(self.frm_eleicao, width=30)
        self.ent_nome.grid(column=1, row=0)

        self.lbl_data_ini = tk.Label(self.frm_eleicao, text='Início:')
        self.lbl_data_ini.grid(column=0, row=1, pady=10)
        self.data_ini = DateEntry(self.frm_eleicao,selectmode='day', date_pattern='dd-MM-yyyy')
        self.data_ini.grid(column=1, row=1)

        self.lbl_data_fim = tk.Label(self.frm_eleicao, text='Fim:')
        self.lbl_data_fim.grid(column=0, row=2, pady=10)
        self.data_fim = DateEntry(self.frm_eleicao, selectmode='day', date_pattern='dd-MM-yyyy')
        self.data_fim.grid(column=1, row=2)

        self.lbl_cargos = tk.Label(self.frm_eleicao, text="Cargos:")
        self.lbl_cargos.grid(column=0, row=3)
        self.cbx_cargo = ttk.Combobox(self.frm_eleicao, width=17)
        query = 'SELECT DISTINCT nome_cargo FROM cargo;'
        valores = bd.consultar_cargos(query)
        self.cbx_cargo['values'] = (f'{valores}')
        self.cbx_cargo.grid(column=1, row=3)
        self.cbx_cargo.current(0)

        self.lbl_desc = tk.Label(self.frm_eleicao, text="Descrição:")
        self.lbl_desc.grid(column=0, row=4, pady=10)
        self.ent_desc = tk.Entry(self.frm_eleicao, width=30)
        self.ent_desc.grid(column=1, row=4)

        self.btn_inserir = tk.Button(self.frm_eleicao, text='Adicionar Eleição', command=self.confirmar_cadastro_eleicao)
        self.btn_inserir.grid(column=0, row=5, columnspan=2)

    def confirmar_cadastro_eleicao(self):
        nome = self.ent_nome.get()
        cargo = self.cbx_cargo.get()
        if nome == '':
            messagebox.showwarning('Aviso', 'Insira o nome da eleição!')
            self.ins_eleicao.deiconify()
        elif len(nome) > 50:
            messagebox.showwarning('Nome muito grande', 'Insira um nome mais curto!')
            self.ins_eleicao.deiconify()
        elif len(self.ent_desc.get()) > 70:
            messagebox.showwarning('Descrição muito grande', 'Insira uma descrição mais breve!')
            self.ins_eleicao.deiconify()
        elif cargo == '':
            messagebox.showwarning('Aviso', 'Selecione um cargo!')
            self.ins_eleicao.deiconify()
        else:
            query = f'INSERT INTO eleicao ("nome", "data_inicio", "descricao", "cargo", "data_fim",  "ativo") VALUES ("{nome}", "{self.data_ini.get()}", "{self.ent_desc.get()}", "{cargo}", "{self.data_fim.get()}", TRUE);'
            bd.inserir(query)
            self.atualizar_tvw_eleicao()
            messagebox.showinfo("Aviso", "Eleição cadastrada com sucesso!")
            self.ins_eleicao.destroy()
            self.eleicoes_mostrar.deiconify()

    def editar_eleicao(self):
        selecionado = self.tvw_eleicao.selection()
        lista = self.tvw_eleicao.item(selecionado, "values")

        self.edit_eleicao = tk.Toplevel()
        self.edit_eleicao.title("Editar candidato")
        self.edit_eleicao.geometry("400x250")
        self.voltar = tk.Button(self.edit_eleicao, text="Voltar", command=self.edit_eleicao.destroy, width=8)
        self.voltar.pack(side=tk.LEFT)

        self.nome = tk.Label(self.edit_eleicao, text="Editar candidato", font=32)
        self.nome.pack()

        self.frm_edit = tk.Frame(self.edit_eleicao)
        self.frm_edit.pack()
        self.lbl_nome = tk.Label(self.frm_edit, text="Nome:")
        self.lbl_nome.grid(column=0, row=0)
        self.ent_nome = tk.Entry(self.frm_edit, width=30)
        self.ent_nome.grid(column=1, row=0)
        self.ent_nome.insert(0, lista[1])

        self.lbl_desc = tk.Label(self.frm_edit, text="Descrição:")
        self.lbl_desc.grid(column=0, row=1, pady=10)
        self.ent_desc = tk.Entry(self.frm_edit, width=30)
        self.ent_desc.grid(column=1, row=1)
        self.ent_desc.insert(0, lista[2])

        # INSERIR A DATA NO CALENDARIO DO DATE ENTRY
        self.lbl_data_ini = tk.Label(self.frm_edit, text='Início:')
        self.lbl_data_ini.grid(column=0, row=2, pady=10)
        self.data_ini = DateEntry(self.frm_edit, selectmode='day', date_pattern='dd-MM-yyyy', day=int(lista[4][:2]), month=int(lista[4][3:5]), year=int(lista[4][6:10]))
        self.data_ini.grid(column=1, row=2)

        self.lbl_data_fim = tk.Label(self.frm_edit, text='Fim:')
        self.lbl_data_fim.grid(column=0, row=3, pady=10)
        self.data_fim = DateEntry(self.frm_edit, selectmode='day', date_pattern='dd-MM-yyyy', day=int(lista[5][:2]), month=int(lista[5][3:5]), year=int(lista[5][6:10]))
        self.data_fim.grid(column=1, row=3)

        self.lbl_cargos = tk.Label(self.frm_edit, text="Cargos:")
        self.lbl_cargos.grid(column=0, row=4, pady=5)
        self.cbx_cargo = ttk.Combobox(self.frm_edit, width=17)
        query = 'SELECT DISTINCT nome_cargo FROM cargo;'
        valores = bd.consultar_cargos(query)
        self.cbx_cargo['values'] = (f'{valores}')
        self.cbx_cargo.grid(column=1, row=4)
        valores = valores.split()
        for i in range(len(valores)):
            if valores[i] == lista[3]:
                self.cbx_cargo.current(i)

        self.btn_con_edi = tk.Button(self.frm_edit, text="Confimar", command=self.confirmar_edit_eleicao)
        self.btn_con_edi.grid(column=0, row=5, columnspan=2, pady=10)

    def confirmar_edit_eleicao(self):
        selecionado = self.tvw_eleicao.selection()
        lista = self.tvw_eleicao.item(selecionado, "values")

        if lista[1] == self.ent_nome.get() and lista[2] == self.ent_desc.get() and lista[4] == self.data_ini.get() and lista[5] == self.data_fim.get() and lista[3] == self.cbx_cargo.get():
            message = messagebox.askyesno("Sem alterações", "Você tem certeza que não deseja realizar nenhuma alteração?")
            if message:
                self.edit_eleicao.destroy()
                self.eleicoes_mostrar.deiconify()
            else:
                self.edit_eleicao.deiconify()
        else:
            message = messagebox.askyesno("Alterações realizadas", "Você tem certeza que deseja realizar as alterações?")
            if message:
                query = f'UPDATE eleicao SET nome="{self.ent_nome.get()}", descricao="{self.ent_desc.get()}", cargo="{self.cbx_cargo.get()}", data_inicio="{self.data_ini.get()}",' \
                        f' data_fim="{self.data_fim.get()}" WHERE eleicao_id={lista[0]};'
                bd.atualizar(query)
                self.atualizar_tvw_eleicao()
                self.edit_eleicao.destroy()
                self.eleicoes_mostrar.deiconify()
            else:
                self.edit_eleicao.deiconify()

    def excluir_eleicao(self):
        selecionado = self.tvw_eleicao.selection()
        lista = self.tvw_eleicao.item(selecionado, "values")
        if selecionado != ():
            mensagem = messagebox.askyesno("Excluir", "Você tem certeza que deseja excluir a eleicao?")
            if mensagem:
                sql = f'DELETE FROM eleicao WHERE eleicao_id={lista[0]};'
                bd.deletar(sql)
                self.atualizar_tvw_eleicao()
                messagebox.showinfo("Excluída", "Eleição excluída com sucesso!")
            self.eleicoes_mostrar.deiconify()

    def atualizar_tvw_eleicao(self):
        for i in self.tvw_eleicao.get_children():
            self.tvw_eleicao.delete(i)
        query = 'SELECT * FROM eleicao;'
        dados = bd.consultar(query)
        for tupla in dados:
            self.tvw_eleicao.insert('', tk.END, values=tupla)

    def pesquisar_tvw_eleicao(self):
        busca = self.ent_pesq.get()
        for i in self.tvw_eleicao.get_children():
            self.tvw_eleicao.delete(i)
        if busca == '':
            self.atualizar_tvw_eleicao()
        else:
            query = f"SELECT * FROM eleicao WHERE nome LIKE '{busca}%';"
            dados = bd.consultar(query)
            #if dados == []:
                #messagebox.showinfo("Sem dados", "Sem correspondencia a busca!")
                #self.mostrar_eleicoes.deiconify()
            #else:
            for tupla in dados:
                self.tvw_eleicao.insert('', tk.END, values=tupla)

    def login(self):
        self.janela.withdraw()
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
        self.login.destroy()
        self.votar = tk.Toplevel()
        self.votar.geometry("800x600")
        self.votar.title("Área de votos")
        self.welcome = tk.Label(self.votar, text="Bem vindo!", font=("Verdana", 24))
        self.welcome.grid(column=0, row=0, padx=300)

        self.frm_votacao = tk.Frame(self.votar)
        self.frm_votacao.grid(column=0, row=1, pady=15)
        self.lbl_eleicoes = tk.Label(self.frm_votacao, text="Eleição:", font=12)
        self.lbl_eleicoes.grid(column=0, row=0)
        self.cbx_eleicoes = ttk.Combobox(self.frm_votacao, width=30, font=12)
        query = 'SELECT nome FROM eleicao WHERE ativo LIKE TRUE;'
        valores = bd.consultar(query)
        listas = [dado for dado, in valores]
        self.cbx_eleicoes['values'] = (listas)
        self.cbx_eleicoes.grid(column=1, row=0)
        self.cbx_eleicoes.current(0)

        self.btn_conf_eleicao = tk.Button(self.frm_votacao, text="Selecionar eleição", command=self.confirmar_escolha_eleicao, font=4)
        self.btn_conf_eleicao.grid(column=0, row=1, columnspan=2, pady=20)

    def confirmar_escolha_eleicao(self):
        query = f'SELECT * FROM eleicao WHERE nome LIKE "{self.cbx_eleicoes.get()}";'
        valores = bd.consultar(query)
        self.frm_show = tk.Frame(self.votar)
        self.frm_show.grid(column=0, row=2)

        self.lbl_nome_eleicao = tk.Label(self.frm_show, text=valores[0][1], width=30, font=38, bg="Black", fg="White")
        self.lbl_nome_eleicao.grid(column=0, row=0, sticky=tk.EW, columnspan=2)

        self.lbl_desc = tk.Label(self.frm_show, text="Descriçao:                     "
                                 , font=28, width=30, bg="Black", fg="White")
        self.lbl_desc.grid(column=0, row=1, sticky=tk.W, columnspan=2)

        self.lbl_desc2 = tk.Label(self.frm_show, text="", font=28, width=30, bg="Black", fg="White")
        self.lbl_desc2.grid(column=1, row=1, sticky=tk.EW)

        self.lbl_descricao = tk.Label(self.frm_show, text=valores[0][2], font=28, width=70, bg="Black", fg="White")
        self.lbl_descricao.grid(column=0, row=2, columnspan=2)

        self.btn_selecionar_eleicao = tk.Button(self.frm_show, text="Votar nesta eleição", font=8, command=self.tela_voto)
        self.btn_selecionar_eleicao.grid(column=0, row=3, columnspan=2, pady=15)

    def tela_voto(self):
        self.votar = tk.Toplevel()
        self.votar.geometry("400x300")
        self.votar.title("Votar")
        self.lbl_voto = tk.Label(self.votar, text="Área de voto", font=32)
        self.lbl_voto.pack()
        self.frm_voto = tk.Frame(self.votar)
        self.frm_voto.pack(pady=15)
        self.lbl_num = tk.Label(self.frm_voto, text="Número do candidato")
        self.lbl_num.grid(column=0, row=0)

        self.ent_num = tk.Entry(self.frm_voto)
        self.ent_num.grid(column=1, row=0)

        self.btn_num = tk.Button(self.frm_voto, text="Buscar", width=8, command=self.buscar_candidato)
        self.btn_num.grid(column=0, row=1, columnspan=2, pady=15)

        #self.frm_black = tk.Frame(self.voto)
        #self.frm_black.pack()
        #self.borda_imagem = tk.PhotoImage(file="imgs/black.png")
        #self.lbl_black = tk.Label(self.voto, image=self.borda_imagem)
        #self.lbl_black.image = self.borda_imagem
        #self.lbl_black.pack()

        self.minha_imagem = tk.PhotoImage(file="imgs/img1.png")
        self.lbl_mostrar_cand = tk.Label(self.frm_voto, image=self.minha_imagem)
        self.lbl_mostrar_cand.image = self.minha_imagem
        self.lbl_mostrar_cand.grid(column=0, row=3)

        self.lbl_nome_candidato = tk.Label(self.frm_voto, text="NOME", width=30)
        self.lbl_nome_candidato.grid(column=0, row=4)

    def buscar_candidato(self):
        self.btn_votar = tk.Button(self.votar, text="Votar")
        self.btn_votar.grid(column=0, row=5)

app = tk.Tk()
Tela(app)
app.mainloop()
# nao pos
# botao reset
# get data para encerrar automaticamente