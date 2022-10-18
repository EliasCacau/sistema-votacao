import tkinter as tk
from tkcalendar import DateEntry

from datetime import datetime

if __name__ == '__main__':

    first = datetime(2022, 10, 18)
    second = datetime.now()

    print(first)
    print(second)

    if first < second:
        print('Primeira data é menor que a segunda')
    elif first > second:
        print('Primeira data é maior que a segunda')
    else:
        print('As datas são iguais.')

# from PIL import Image
# img = Image.open('imgs/refresh.png')
# img = img.resize((15, 15), Image.ANTIALIAS)
# img.save('imgs/refresh.png')

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

