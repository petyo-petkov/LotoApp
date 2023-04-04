import cv2
from pyzbar.pyzbar import decode
import db
from datetime import datetime


class Captura:

    @staticmethod
    def captur_qr_code():
        cap = cv2.VideoCapture(0)
        success = True
        while success:
            # leyendo y decodificando la img.
            success, img = cap.read()
            for barcode in decode(img):
                qr_data = barcode.data.decode('utf-8')
                qr_data = qr_data.split(';')
                # preparando eldata para los decimos de la loteria
                if len(qr_data) == 1:
                    qr_data = f'{qr_data[0][2:]} P={qr_data[0][0]} {0} {0} {0} {0} {0} {0} {0}'
                    qr_data = qr_data.split(' ')

                print(qr_data)
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
            combinaciones = qr_data[4]
            combinaciones = combinaciones.split('.')
            del combinaciones[0]
            precio = int((1 * len(combinaciones) * int(qr_data[2][-1])))

            boleto_primitiva = {"sn": qr_data[0],
                                "fecha": qr_data[2][5:12],
                                "combinaciones": combinaciones,
                                "reintegro": qr_data[6],
                                "joker": qr_data[7],
                                "dias_jugados": qr_data[2][-1],
                                "precio": precio,
                                "tipo": "Primitiva",
                                "fecha insercion": datetime.utcnow()}
            return boleto_primitiva

        def bonoloto():
            combinaciones = qr_data[4]
            combinaciones = combinaciones.split('.')
            del combinaciones[0]
            precio = float((0.5 * len(combinaciones) * int(qr_data[2][-1])))

            boleto_bonoloto = {"sn": qr_data[0],
                               "fecha": qr_data[2][5:12],
                               "combinaciones": combinaciones,
                               "reintegro": qr_data[6],
                               "joker": qr_data[7],
                               "dias_jugados": qr_data[2][-1],
                               "precio": precio,
                               "tipo": "Bonoloto",
                               "fecha insercion": datetime.utcnow()}
            return boleto_bonoloto

        def loteria():
            if 'P=5' in qr_data:
                precio = 15
            if 'P=6' in qr_data:
                precio = 3
            boleto_loteria = {"sn": qr_data[0],
                              "numero": qr_data[0][9:14],
                              "fecha": qr_data[0][:2],
                              "precio": precio,
                              "tipo": "Loteria",
                              "fecha insercion": datetime.utcnow()}
            return boleto_loteria

        def euromillon():
            combinaciones = qr_data[4]
            combinaciones = combinaciones.split('.')
            del combinaciones[0]

            boleto_euromillones = {"sn": qr_data[0],
                                   "fecha": qr_data[2][5:12],
                                   "combinaciones": combinaciones,
                                   "num_millon": qr_data[6][21:29],
                                   "dias_jugados": qr_data[2][-1],
                                   "precio": (2.5 * len(combinaciones)) * int(qr_data[2][-1]),
                                   "tipo": "Euromillones",
                                   "fecha insercion": datetime.utcnow()}
            return boleto_euromillones

        if 'P=5' in qr_data[1]:
            boleto = loteria()
        if 'P=6' in qr_data[1]:
            boleto = loteria()
        if 'P=1' in qr_data[1]:
            boleto = primitiva()
        if 'P=7' in qr_data[1]:
            boleto = euromillon()
        if 'P=2' in qr_data[1]:
            boleto = bonoloto()

        # comprobando si el boletos existe en la DB y lo añadimos en caso que no.
        if qr_data[0] not in db.toto.distinct("sn"):
            db.toto.insert_one(boleto)
            print('Boleto añadido correctamente')
        else:
            print("Ya existe este boleto")

    # creando documento (con la suma de los boletos) en la DB
    @staticmethod
    def sum_precios() -> None:
        # sumando los precios de los boletos
        cursor = db.toto.find({})
        suma = 0
        for i in cursor:
            precios = float(i["precio"])
            suma = suma + precios

        gastado = {"gastado": suma,
                   "date": datetime.utcnow()}

        # actualizando la suma de los boletos
        try:
            old = db.gastos.find_one()
            new = {"$set": gastado}
            db.gastos.update_one(old, new)

        except:
            db.gastos.insert_one(gastado)
