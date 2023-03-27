import cv2
from pyzbar.pyzbar import decode
import db
from datetime import datetime


class Captura:

    @staticmethod
    def captura():
        cap = cv2.VideoCapture(0)
        success = True
        while success:
            # leyendo y decodificando la img.
            success, img = cap.read()
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                myData = myData.split(';')
                # preparando eldata para los decimos de la loteria
                if len(myData) == 1:
                    myData = f'{myData[0][2:]} P={myData[0][0]} {0} {0} {0} {0} {0} {0} {0}'
                    myData = myData.split(' ')

                print(myData)
                success = False

            # mostrando los resultados
            cv2.namedWindow("Scann", cv2.WINDOW_NORMAL)  # para mostrar ventana mas pequieña.
            cv2.imshow('Scann', img)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

        # BOLETOS
        def primitiva():
            combinaciones = myData[4]
            combinaciones = combinaciones.split('.')
            del combinaciones[0]
            precio = int((1 * len(combinaciones) * int(myData[2][-1])))

            boleto_primitiva = {"sn": myData[0],
                                "fecha": myData[2][5:12],
                                "combinaciones": combinaciones,
                                "reintegro": myData[6],
                                "joker": myData[7],
                                "dias_jugados": myData[2][-1],
                                "precio": precio,
                                "tipo": "Primitiva",
                                "fecha insercion": datetime.utcnow()}
            return boleto_primitiva

        def bonoloto():
            combinaciones = myData[4]
            combinaciones = combinaciones.split('.')
            del combinaciones[0]
            precio = float((0.5 * len(combinaciones) * int(myData[2][-1])))

            boleto_bonoloto = {"sn": myData[0],
                               "fecha": myData[2][5:12],
                               "combinaciones": combinaciones,
                               "reintegro": myData[6],
                               "joker": myData[7],
                               "dias_jugados": myData[2][-1],
                               "precio": precio,
                               "tipo": "Bonoloto",
                               "fecha insercion": datetime.utcnow()}
            return boleto_bonoloto

        def loteria():
            if myData[1] == 'P=5':
                precio_boleto = 6
            if myData[1] == 'P=6':
                precio_boleto = 3

            boleto_loteria = {"sn": myData[0],
                              "numero": myData[0][9:14],
                              "fecha": myData[0][:2],
                              "precio": precio_boleto,
                              "tipo": "Loteria",
                              "fecha insercion": datetime.utcnow()}
            return boleto_loteria

        def euromillon():
            combinaciones = myData[4]
            combinaciones = combinaciones.split('.')
            del combinaciones[0]

            boleto_euromillones = {"sn": myData[0],
                                   "fecha": myData[2][5:12],
                                   "combinaciones": combinaciones,
                                   "num_millon": myData[6][21:29],
                                   "dias_jugados": myData[2][-1],
                                   "precio": (2.5 * len(combinaciones)) * int(myData[2][-1]),
                                   "tipo": "Euromillones",
                                   "fecha insercion": datetime.utcnow()}
            return boleto_euromillones

        if 'P=6' in myData[1]:
            boleto = loteria()
        if 'P=1' in myData[1]:
            boleto = primitiva()
        if 'P=7' in myData[1]:
            boleto = euromillon()
        if 'P=2' in myData[1]:
            boleto = bonoloto()

        # comprobando si el boletos existe en la DB y lo añadimos en caso que no.
        if myData[0] not in db.toto.distinct("sn"):
            db.toto.insert_one(boleto)
            print('Boleto añadido correctamente')
        else:
            print("Ya existe este boleto")

    # creando documento (con la suma de los boletos) en la DB
    @staticmethod
    def sumPrecios() -> None:
        # sumando los precios de los boletos
        precios = db.toto.distinct("precio")
        suma = sum(precios)
        gastado = {"gastado": suma,
                   "date": datetime.utcnow()}

        # actualizando la suma de los boletos
        try:
            old = db.gastos.find_one()
            new = {"$set": gastado}
            db.gastos.update_one(old, new)

        except:
            db.gastos.insert_one(gastado)
