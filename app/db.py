from flask import g, current_app
from flask_pymongo import PyMongo
from pymongo import MongoClient

db_client = MongoClient(host="localhost", port=27017).get_database(name="expenseTracker")

def get_transac_por_concepto(concepto):
    return db_client.get_collection(name="transactions").find(filter={"Concepto":{"$regex":f".*{concepto}.*"}}, projection={"Concepto":1, "Importe":1, "Fecha":1, "_id":0}, limit=400).to_list()

