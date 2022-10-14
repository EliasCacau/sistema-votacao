import tkinter as tk
from tkcalendar import DateEntry

my_w = tk.Tk()
my_w.geometry("340x220")

cal=DateEntry(my_w,selectmode='day')
cal.grid(row=1,column=1,padx=15)
btn = tk.Button(my_w, text="Confirmar")
btn.grid(row=2, column=1)
dt=cal.get_date()
str_dt4 = dt.strftime("%Y-%m-%d") # 2021-04-18(For Database query)
print(str_dt4)
my_w.mainloop()

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

