from pymongo import MongoClient

cliente = MongoClient(
    "http://localhost/127.0.0.1"
)

db = cliente.loto
toto = db.toto
gastos = db.gastos

