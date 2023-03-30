import db
import customtkinter

n = db.toto.count_documents({})


def ver():
    lst = [['tipo', 'precio', 'fecha']]
    cursor = db.toto.find({}, {'_id': False})
    for datos in cursor:
        tipo_db = str(datos['tipo'])
        precio_db = str(datos['precio'])
        fecha_db = str(datos['fecha'])
        lst.append([tipo_db, precio_db, fecha_db])

    for i in range(len(lst)):
        for j in range(len(lst[0])):
            mgrid = customtkinter.CTkEntry(frame, width=150, height=20)
            #mgrid._values = mgrid.get(), i
            mgrid.insert(customtkinter.END, lst[i][j])
            mgrid.grid(row=i+7, column=j+6)




root = customtkinter.CTk()
root.geometry('500x320')

frame = customtkinter.CTkFrame(root)
frame.after(1000, ver())

frame.grid()


root.mainloop()