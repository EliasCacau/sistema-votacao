import os
from PIL import Image
from tkinter import filedialog as fd
import tkinter as tk
class Teste():
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("300x200")

        #self.button = tk.Button(self.janela, text="Abrir").pack()
        tipos = (('Imagem', '*.PNG'), ('Imagem', '*.JPG'), ('Todos', '*.*'))
        self.imagem = fd.askopenfilename(initialdir=f'/imgs', filetypes=tipos)
        img = Image.open(self.imagem)
        self.imagem = self.imagem.replace(".jpg","")
        img.save(f"imgs/{self.imagem}.png")

app = tk.Tk()
Teste(app)
app.mainloop()