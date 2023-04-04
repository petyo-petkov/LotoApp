import db
import tkinter

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
            mgrid = tkinter.Entry(frame, background='black', relief='ridge', fg='white')
            #mgrid._values = mgrid.get(), i
            mgrid.insert(tkinter.END, lst[i][j])
            mgrid.grid(row=i+7, column=j+6)




root = tkinter.Tk()
root.geometry('500x320')


frame = tkinter.Frame(root, background='black', height=300, width=150)
frame.pack()
frame.after(1000, ver())

button1 = tkinter.Button(root, text='ADD')
button1.pack()

box = tkinter.Checkbutton(root)
box.pack()

root.mainloop()