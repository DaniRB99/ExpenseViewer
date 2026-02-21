import csv
from pymongo import MongoClient

#TODO: reglas de validación en mongo
#TODO: validación datos
    # conversor de caracteres machacados
    # conversor double a int
    # procesar saldo total (quitar particula EUR)
    # validar que no se dupliquen las transacciones
    # carga fecha como DATE
    
#TODO: CREAR CONEXIÓN - DB
# class MongoConn:
#     def __init__(self):
#         self.host:str = "localhost"
#         self.port:str = 27017
#         self.db:str = "expenseTracker"
    
#     def createConnection(self, db:str=None):
#         self.client = MongoClient(host=self.host, port=self.port)
#         db_conn = db if not None else self.db
#         self.database = self.client.get_database(name=db_conn)
        
#     def getCollection(self, collection:str):
#         return self.database.get_collection(name=collection)
    
#TODO: ABRIR EXCEL EN MEMORIA cargarlo


#TODO: adaptación de datos

#TODO: CRUCE - Revisar si ya existen

#TODO: CARGA - bucle registro leido - registro cargado en mongo

if __name__ == "__main__":
    movs:list = []
    with open('csv/TT171225.554.csv', mode ='r',encoding='UTF-8') as file:    
        movs = list(csv.DictReader(file, delimiter=","))
        
    print(f"Number of transactions: {len(movs)}")

    #importar
    client = MongoClient(host="localhost", port=27017)
    db = client.get_database(name="expenseTracker")
    collection = db.get_collection(name="transactions")
    print(f"Cargando transacciones en {client.address}")
    result = collection.insert_many(movs)
    print(f"Carga completada: {len(result.inserted_ids)}")
    