import tkinter as tk
from tkcalendar import DateEntry

from datetime import datetime


# file = open("apuracao_votos/new_file.txt", "x")
# file.write("\nNova linha")
# file.close()

# if __name__ == '__main__':
#
#     first = datetime(2022, 10, 18)
#     second = datetime.now()
#
#     print(first)
#     print(second)
#
#     if first < second:
#         print('Primeira data é menor que a segunda')
#     elif first > second:
#         print('Primeira data é maior que a segunda')
#     else:
#         print('As datas são iguais.')

from PIL import Image
# for i in range(1,6):
img = Image.open(f'imgs/img1.png')
img = img.resize((150, 150), Image.ANTIALIAS)
img.save(f'imgs/img1.png')

# import os
# from PIL import Image
# from tkinter import filedialog as fd
# import tkinter as tk
# class Teste():
#     def __init__(self, master):
#         self.janela = master
#         self.janela.geometry("300x200")
#
#         #self.button = tk.Button(self.janela, text="Abrir").pack()
#         tipos = (('Imagem', '*.PNG'), ('Imagem', '*.JPG'), ('Todos', '*.*'))
#         self.imagem = fd.askopenfilename(initialdir=f'/imgs', filetypes=tipos)
#         img = Image.open(self.imagem)
#         self.imagem = self.imagem.replace(".jpg","")
#         img.save(f"imgs/{self.imagem}.png")
#
# app = tk.Tk()
# Teste(app)
# app.mainloop()

