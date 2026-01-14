from flask import g, current_app
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime, timedelta
from pytz import timezone, utc
import pprint

db_client = MongoClient(host="localhost", port=27017).get_database(name="expenseTracker")
TRANS_COLLECTION = "transactions_norm"
europeTZ = timezone("Europe/Madrid")

def get_transac_por_concepto(concepto):
    return db_client.get_collection(name="transactions").find(filter={"Concepto":{"$regex":f".*{concepto}.*"}}, 
                                                              projection={"Concepto":1, "Importe":1, "Fecha":1, "_id":0}, limit=400).to_list()

def get_balance():
    return db_client.get_collection(name=TRANS_COLLECTION).find(filter={}
                                            , projection={"saldo":1, 
                                                          "divisa":1, 
                                                          "_id":0}).sort({"fecha_transaccion":-1}).limit(1).to_list()[0]

#new Date(new Date().setDate(new Date().getDate() - 30))
#TODO: agregación con la descripción de los tipos. 
def get_transacs(last_days:int = 60)-> list[dict]:
    pipeline = [
            {
                "$match":
                {
                    "fecha_transaccion": {
                    "$gte": datetime.now() - timedelta(days=last_days)
                    }
                }
            },
            {
                "$lookup": {
                "as": "desc_concepto_comun",
                "from": "code_translate",
                "foreignField": "code",
                "localField": "concepto_comun",
                "pipeline": [
                    {
                    "$match": {
                        "type": "concepto_comun"
                    }
                    }
                ]
                }
            },
            {
                "$lookup": {
                "from": "code_translate",
                "localField": "concepto_propio",
                "foreignField": "code",
                "as": "desc_concepto_propio",
                "pipeline": [
                    {
                    "$match": {
                        "type": "concepto_propio"
                    }
                    }
                ]
                }
            },
            {
                "$addFields":
                {
                    "desc_concepto": {
                    "$concatArrays": [
                        "$desc_concepto_propio",
                        "$desc_concepto_comun"
                    ]
                    }
                }
            },
            {
                "$set":
                {
                    "desc_concepto_compuesto": {
                    "$reduce": {
                        "input": "$desc_concepto.description",
                        "initialValue": "",
                        "in": {
                        "$concat": [
                            "$$this",
                            " | ",
                            "$$value"
                        ]
                        }
                    }
                    }
                }
            },
            {  #FIXME: normalizar datos: NO SE PUEDE TENER MÁS DE UN DESTINATARIO - FALTA EMISOR
                "$project":
                {
                    "_id":1,
                    "num_cuenta": 1,
                    "divisa": 1,
                    "fecha_transaccion": 1,
                    "importe": 1,
                    "saldo": 1,
                    "referencia": "$ref_2",
                    "destinatario_1": "$concepto_1",
                    "desc_usuario": "$concepto_5",
                    "destinatario_2": "$concepto_9",
                    "desc_concepto_compuesto": 1
                }
            }
            ]
    # db_client.get_collection(name=TRANS_COLLECTION).find(filter={"fecha_transaccion":{"$gte": datetime.now() - timedelta(days=-30)}},
    #                                                        projection={"_id":1, "num_cuenta":1, "divisa":1, "fecha_transaccion":1, "importe":1, "concepto_comun":1})
    
    # return db_client.get_collection(name=TRANS_COLLECTION).find(filter={"fecha_transaccion":{"$gte": utc.localize( datetime.now() - timedelta(days=-30)).astimezone(europeTZ)}},
    #                                                        projection={"_id":0, "num_cuenta":1, "divisa":1, "fecha_transaccion":1, "importe":1, "concepto_comun":1}).to_list()
    
    return db_client.get_collection(name=TRANS_COLLECTION).aggregate(pipeline=pipeline).to_list()

if __name__ == "__main__":
    pprint.pprint(get_transacs())
    