# import json
# import tkinter
# from bson import json_util
from tkinter import messagebox
import customtkinter
import db
from app import Captura
from delete import Delete

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

gastado = f'{db.gastos.distinct("gastado")} euros'.replace('[', '').replace(']', '')


def add():
    Captura.captura()
    Captura.sumPrecios()
    ver(1)
    ver(0)
    mostrar_gastado()


# def mostrar_boletos():
#    cursor = db.toto.find({}, {'_id': False})
#    return str(json.dumps(list(cursor), default=json_util.default, indent=1))


def cancel():
    yes = messagebox.askyesno("Salir", "Salir ?")
    if yes:
        quit()


def delete():
    yes = messagebox.askyesno("Borrar", "Borrar TODO ?")
    if yes:
        Delete.deleteAll()
        Delete.deleteGastado()
    ver(1)
    ver(0)
    mostrar_gastado()


def ver(n):
    lst = [['TIPO', 'PRECIO', 'FECHA']]
    cursor = db.toto.find({}, {'_id': False})
    for datos in cursor:
        tipo_db = str(datos['tipo'])
        precio_db = str(datos['precio'])
        fecha_db = str(datos['fecha'])
        lst.append([tipo_db, precio_db, fecha_db])

    for i in range(len(lst)):
        for j in range(len(lst[0])):
            mgrid = customtkinter.CTkEntry(text_frame, width=155, height=28, text_color='black', fg_color='#F4F6F7',
                                           corner_radius=4)
            mgrid.insert(customtkinter.END, lst[i][j])
            mgrid.grid(row=i + 0, column=j + 1)
    if n == 1:
        for label in text_frame.grid_slaves():
            # if int(label.grid_info()["row"]) > 6:  ## dejar solo los row indicados (6)
            label.grid_forget()


def mostrar_gastado():
    Captura.sumPrecios()
    campo_gastado = customtkinter.CTkEntry(side_frame, width=150, height=30,
                                           text_color="black", fg_color="#F4F6F7")
    campo_gastado.grid(row=1, column=0, padx=10, pady=(0, 20))
    campo_gastado.insert(customtkinter.END,
                         f'{db.gastos.distinct("gastado")} euros'.replace('[', '').replace(']', ''))


# config. window
root = customtkinter.CTk()
root.title("LotoApp")
root.iconbitmap('@logo.xbm')
root.geometry("680x420")
root.resizable(width=False, height=False)

# config. side_frame
side_frame = customtkinter.CTkFrame(root, width=200, height=340, fg_color="#F7DC6F")
side_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
side_frame.grid_rowconfigure(4, weight=1)

text_frame = customtkinter.CTkFrame(root, width=460, height=340)
text_frame.grid(row=0, column=1, rowspan=9, columnspan=3, padx=10, pady=10, sticky="nsew")
ver(0)
mostrar_gastado()
# textbox ganado-gastado
# textbox_gastado = customtkinter.CTkEntry(side_frame, width=150, height=30,
#                                            text_color="black", fg_color="#F4F6F7")
# textbox_gastado.grid(row=1, column=0, padx=10, pady=(0, 20))
# textbox_gastado.after(1000, mostrar_gastado())

gastado_label = customtkinter.CTkLabel(side_frame, text="GASTADO", text_color="#17202A")
gastado_label.grid(row=0, column=0)

textbox_ganado = customtkinter.CTkTextbox(side_frame, width=150, height=20,
                                          activate_scrollbars=False, text_color="black", fg_color="#F4F6F7")
textbox_ganado.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="n")
ganado_label = customtkinter.CTkLabel(side_frame, text="GANADO", text_color="#17202A")
ganado_label.grid(row=2, column=0)

# botones
button_new = customtkinter.CTkButton(root, width=100, height=30, text="NUEVO", text_color="#17202A",
                                     fg_color="#27AE60", hover_color="#229954")
button_new.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

button_add = customtkinter.CTkButton(root, width=100, height=30, text="AÑADIR", text_color="#17202A",
                                     fg_color="#27AE60", hover_color="#229954", command=add)
button_add.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

button_borrar = customtkinter.CTkButton(root, width=100, height=30, text="BORRAR", text_color="#17202A",
                                        fg_color="#E74C3C", hover_color="#FE1800", command=delete)
button_borrar.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

button_salir = customtkinter.CTkButton(root, width=100, height=30, text="SALIR",
                                       text_color="#17202A", fg_color="#F4D03F", hover_color="#F1C40F",
                                       command=cancel)
button_salir.grid(row=8, column=0, padx=10, pady=10, sticky="nsew")

# set default
# textbox_gastado.configure(state="disabled")
textbox_ganado.configure(state="disabled")

root.mainloop()
