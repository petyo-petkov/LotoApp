from pymongo import MongoClient

cliente = MongoClient(
    "mongodb://localhost:27017"
)

db = cliente.loto
toto = db.toto
gastos = db.gastos

