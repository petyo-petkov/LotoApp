from tkinter import messagebox
import customtkinter
import db
from app import Captura
from delete import Delete

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


def add_boleto():
    Captura.captur_qr_code()
    Captura.sum_precios()
    info_boletos(1)
    info_boletos(0)
    mostrar_gastado()


""" mostrar los boletos como json 
    def mostrar_boletos():
       cursor = db.toto.find({}, {'_id': False})
    return str(json.dumps(list(cursor), default=json_util.default, indent=1))
"""


def cancel():
    yes = messagebox.askyesno("Salir", "Salir ?")
    if yes:
        quit()


def delete():
    yes = messagebox.askyesno("Borrar", "Borrar TODO ?")
    if yes:
        Delete.deleteAll()
        Delete.deleteGastado()
    info_boletos(1)
    info_boletos(0)
    mostrar_gastado()


def info_boletos(n):
    lst = [['ID', 'TIPO', 'PRECIO', 'FECHA']]
    cursor = db.toto.find({})
    for datos in cursor:
        id_db = str(datos['_id'])
        tipo_db = str(datos['tipo'])
        precio_db = f" {datos['precio']} \N{euro sign}"  # " \N{euro sign} " - muestra el signo del euro
        fecha_db = str(datos['fecha'])
        lst.append([id_db, tipo_db, precio_db, fecha_db])

    for i in range(len(lst)):
        for j in range(len(lst[0])):
            mgrid = customtkinter.CTkEntry(text_frame, width=165, height=28, text_color='black', fg_color='#F4F6F7',
                                           corner_radius=4)
            mgrid.insert(customtkinter.END, lst[i][j])
            mgrid.grid(row=i + 0, column=j + 1, pady=2)
    if n == 1:
        for label in text_frame.grid_slaves():
            # if int(label.grid_info()["row"]) > 6:  ## dejar solo los row indicados (6)
            label.grid_forget()


def mostrar_gastado():
    Captura.sum_precios()
    campo_gastado = customtkinter.CTkEntry(side_frame, width=100, height=32, corner_radius=4,
                                           text_color="black", fg_color="#F4F6F7")
    campo_gastado.grid(row=1, column=0, padx=10, pady=(0, 20))
    campo_gastado.insert(customtkinter.END,
                         f'{db.gastos.distinct("gastado")} \N{euro sign}'.replace('[', '').replace(']', ''))


# config. window
root = customtkinter.CTk()
root.title("LotoApp")
root.geometry("800x420")
root.resizable(width=False, height=False)

# config. side_frame
side_frame = customtkinter.CTkFrame(root, width=150, height=340, fg_color="#F7DC6F")
side_frame.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="nsew")
side_frame.grid_rowconfigure(4, weight=1)

# config. text_frame
text_frame = customtkinter.CTkFrame(root, width=460, height=340)
text_frame.grid(row=0, column=1, rowspan=9, columnspan=3, padx=5, pady=5, sticky="nsew")
info_boletos(0)
mostrar_gastado()

gastado_label = customtkinter.CTkLabel(side_frame, text="GASTADO", text_color="#17202A")
gastado_label.grid(row=0, column=0)

textentry_ganado = customtkinter.CTkEntry(side_frame, width=100, height=32, corner_radius=4,
                                        text_color="black", fg_color="#F4F6F7")
textentry_ganado.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="n")
ganado_label = customtkinter.CTkLabel(side_frame, text="GANADO", text_color="#17202A")
ganado_label.grid(row=2, column=0)

# botones
button_new = customtkinter.CTkButton(root, width=100, height=30, text="NUEVO", text_color="#17202A",
                                     fg_color="#27AE60", hover_color="#229954")
button_new.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

button_add = customtkinter.CTkButton(root, width=100, height=30, text="AÑADIR", text_color="#17202A",
                                     fg_color="#27AE60", hover_color="#229954", command=add_boleto)
button_add.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

button_borrar = customtkinter.CTkButton(root, width=100, height=30, text="BORRAR", text_color="#17202A",
                                        fg_color="#E74C3C", hover_color="#FE1800", command=delete)
button_borrar.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

button_salir = customtkinter.CTkButton(root, width=100, height=30, text="SALIR",
                                       text_color="#17202A", fg_color="#F4D03F", hover_color="#F1C40F",
                                       command=cancel)
button_salir.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")

# app version label
app_ver = customtkinter.CTkLabel(root, text='LotoApp v.1.0', text_color='white', font=('Roboto', 10))
app_ver.grid(row=9, column=3, sticky='se', padx=5)

root.mainloop()
