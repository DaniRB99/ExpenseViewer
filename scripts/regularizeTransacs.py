from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import  ObjectId
from bson.json_util import dumps
from typing import TypedDict, NotRequired, re
from datetime import datetime, date
from pytz import timezone, utc
import locale


class Transac(TypedDict):
    origen_id:str
    num_cuenta:str
    oficina:int
    divisa:str
    # fecha_operacion:datetime
    fecha_valor:datetime
    fecha_transaccion:NotRequired[datetime]
    importe:float
    saldo:float
    concepto_comun:str
    concepto_propio:str
    ref_1:str
    ref_2:str
    concepto_1:NotRequired[str]
    concepto_2:NotRequired[str]
    concepto_3:NotRequired[str]
    concepto_4:NotRequired[str]
    concepto_5:NotRequired[str]
    concepto_6:NotRequired[str]
    concepto_7:NotRequired[str]
    concepto_8:NotRequired[str]
    concepto_9:NotRequired[str]
    concepto_10:NotRequired[str]

def getLocalTime(date_str:str):
    local_time = None
    try:
        europeTZ = timezone("Europe/Madrid")
        date_date = datetime.strptime(date_str.replace("-","/"),f"%d/%m/%Y")
        local_time =  utc.localize(date_date).astimezone(europeTZ)
    except Exception as err:
        print(err.args[0])
    return local_time


def getFechaTransaccion(concepto:str, default:str = None)->date:
    fecha_date = None
    try:
        literal_str = "Fecha de operación: "
        #14-12-2025
        fecha = concepto[concepto.index(literal_str) + len(literal_str):concepto.index(literal_str) + len(literal_str)+10].strip()
        fecha_date = fecha
    except ValueError as err:
        print(f"Fecha transacción: {err.args[0]}")
        fecha_date = default
    return getLocalTime(fecha_date)

def getConcepto(concepto:str)->str:
    concepto_norm:str = ""
    try:
        literal_str = "Fecha de operación: "
        #14-12-2025
        concepto_norm = concepto[concepto.index(literal_str) + len(literal_str)+11:].strip()
    except ValueError:
        concepto_norm = concepto
    return concepto_norm

def getImporteSaldo(positivo:str, negativo:str):
    res = 0
    try:
        positivo_num = locale.atof(positivo) if positivo != "" else 0
        negativo_num = -locale.atof(negativo) if negativo != "" else 0
        res = positivo_num + negativo_num
    except ValueError as err:
        print(err.args[0])
    return res

if __name__ == "__main__":
    #leer transacciones
    locale.setlocale(locale.LC_ALL,'')
    client = MongoClient(host="localhost", port=27017)
    db = client.get_database(name="expenseTracker")
    transacs = db.get_collection(name="transactions")
    transacs_norm = db.get_collection(name="transactions_norm")
    
    print(f"Conectado a {client.address}/{db.name} leyendo {transacs.name}")
    
    id_normalized = list(map(lambda transac: ObjectId(transac.get("origen_id")), 
                        transacs_norm.find(filter = {}, projection={"origen_id":1, "_id":0})))
    
    print(id_normalized)
    transacs_not_norm = transacs.find(filter={"$and":[
        {"_id":{"$not":{"$in":id_normalized}}},
        # {"_id":{"$eq":ObjectId("694fa42c9ca3235ae089983e")}}
        ]})
    print("Lectura completada")
    
    for transac in transacs_not_norm:
        try:
            print("\n --> Nueva transacción:")
            new_transac = Transac(origen_id=str(transac.get("_id","")),
                                num_cuenta=transac.get("\ufeffN\u00famero de cuenta"),
                                oficina=transac.get("Oficina"),
                                divisa=transac.get("Divisa"),
                                fecha_valor=getLocalTime(transac.get("F. Valor")),
                                fecha_transaccion=getFechaTransaccion(transac.get("Concepto complementario 1"),transac.get("F. Operaci\u00f3n")),
                                importe=getImporteSaldo(transac.get("Ingreso (+)"),transac.get("Gasto (-)")),
                                saldo=getImporteSaldo(transac.get("Saldo (+)"),transac.get("Saldo (-)")),
                                concepto_comun=transac.get("Concepto com\u00fan"),
                                concepto_propio=transac.get("Concepto propio"),
                                ref_1=transac.get("Referencia 1"),
                                ref_2=transac.get("Referencia 2").strip(),
                                concepto_1=getConcepto(transac.get("Concepto complementario 1")),
                                concepto_2=transac.get("Concepto complementario 2").strip(),
                                concepto_3=transac.get("Concepto complementario 3").strip(),
                                concepto_4=transac.get("Concepto complementario 4").strip(),
                                concepto_5=transac.get("Concepto complementario 5").strip(),
                                concepto_6=transac.get("Concepto complementario 6").strip(),
                                concepto_7=transac.get("Concepto complementario 7").strip(),
                                concepto_8=transac.get("Concepto complementario 8").strip(),
                                concepto_9=transac.get("Concepto complementario 9").strip(),
                                concepto_10=transac.get("Concepto complementario 10").strip(),
                                )
            print(new_transac)
            transacs_norm.insert_one(new_transac)
        except DuplicateKeyError as err:
            print(f"!!! ERROR Clave duplicada: {err.details.get("errmsg")}")
            break