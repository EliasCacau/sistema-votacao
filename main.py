import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as ms

janela = tk.Tk()
janela.title('Mostrar nome')
janela.geometry('300x150')

def abrir_arquivo():
    tipos = (('Imagem', '*.PNG'), ('Todos', '*.*'))
    nome = fd.askopenfilename(initialdir='C:/Users/andre/PycharmProjects/sistema-votacao/imgs', filetypes=tipos)
    minha_imagem = tk.PhotoImage(file=f"{nome}")
    lbl = tk.Label(janela, image=minha_imagem)
    lbl.image = minha_imagem
    lbl.pack()

btn = tk.Button(janela, text='Selecionar', command=abrir_arquivo)
btn.pack(expand=True)



janela.mainloop()