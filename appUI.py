import json
import tkinter
from tkinter import messagebox
import customtkinter
from bson import json_util
import db
from app import Captura
from delete import Delete

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


def add():
    Captura.captura()
    Captura.sumPrecios()


def mostrar_boletos():
    cursor = db.toto.find({}, {'_id': False})
    return str(json.dumps(list(cursor), default=json_util.default, indent=1))


def cancel():
    yes = messagebox.askyesno("Salir", "Salir ?")
    if yes:
        quit()


def delete():
    yes = messagebox.askyesno("Borrar", "Borrar TODO ?")
    if yes:
        Delete.deleteAll()
        Delete.deleteGastado()


def mostrar_gastado():
    Captura.sumPrecios()
    textbox_gastado.insert(customtkinter.END,
                           text=f'{db.gastos.distinct("gastado")}euros'.replace('[', '').replace(']', ' '))



# config. window
root = customtkinter.CTk()
root.title("LotoApp")
root.iconbitmap('@logo.xbm')
root.geometry("680x420")
root.resizable(width=False, height=False)

# config. side_frame
side_frame = customtkinter.CTkFrame(root, width=200, height=340, fg_color="#F7DC6F")
side_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
side_frame.grid_rowconfigure(3, weight=1)

# textbox ganado-gastado
textbox_gastado = customtkinter.CTkTextbox(side_frame, width=150, height=20,
                                           activate_scrollbars=False, text_color="black",
                                           fg_color="#F4F6F7")
textbox_gastado.grid(row=1, column=0, padx=10, pady=(0, 20))

# textbox_gastado.insert(customtkinter.END,
#                       text=f'{db.gastos.distinct("gastado")}euros'.replace('[', '').replace(']', ' '))

textbox_gastado.after(1000, mostrar_gastado())

gastado_label = customtkinter.CTkLabel(side_frame, text="GASTADO", text_color="#17202A")
gastado_label.grid(row=0, column=0)

textbox_ganado = customtkinter.CTkTextbox(side_frame, width=150, height=20,
                                          activate_scrollbars=False, text_color="black",
                                          fg_color="#F4F6F7")
textbox_ganado.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="n")
ganado_label = customtkinter.CTkLabel(side_frame, text="GANADO", text_color="#17202A")
ganado_label.grid(row=2, column=0)

# textbox info boletos
textbox_boletos = customtkinter.CTkTextbox(root, width=460, height=340,
                                           fg_color="#F4F6F7", text_color="black")
textbox_boletos.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="nsew")
textbox_boletos.insert(customtkinter.END, mostrar_boletos())

# botones
button_new = customtkinter.CTkButton(root, width=100, height=30, text="NUEVO", text_color="#17202A",
                                     fg_color="#27AE60", hover_color="#229954")
button_new.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

button_add = customtkinter.CTkButton(root, width=100, height=30, text="AÑADIR", text_color="#17202A",
                                     fg_color="#27AE60", hover_color="#229954", command=add)
button_add.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

button_borrar = customtkinter.CTkButton(root, width=100, height=30, text="BORRAR", text_color="#17202A",
                                        fg_color="#E74C3C", hover_color="#FE1800", command=delete)
button_borrar.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

button_cancelar = customtkinter.CTkButton(root, width=100, height=30, text="SALIR",
                                          text_color="#17202A", fg_color="#F4D03F", hover_color="#F1C40F",
                                          command=cancel)
button_cancelar.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

# set default
textbox_gastado.configure(state="disabled")
textbox_ganado.configure(state="disabled")
textbox_boletos.configure(state="disabled")

root.mainloop()
