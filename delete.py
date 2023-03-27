import db


class Delete:
    @staticmethod
    def deleteAll():
        db.toto.delete_many({})
    @staticmethod
    def deleteOne():
        db.toto.delete_one({"sn": "143060010754786009"})
    @staticmethod
    def deleteGastado():
        db.gastos.delete_one({})

