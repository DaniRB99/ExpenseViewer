from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import  ObjectId
from bson.json_util import dumps
from typing import TypedDict, NotRequired
from datetime import datetime, date
from pytz import timezone, utc
from pathlib import Path
import csv
import locale
import re

class TransacNormalization:
    concept_1_dest:list[str] = ["040","038","001","005","044","036"] 
    concept_9_dest:list[str] = ["002","041","067"]
    default_dest:str = "concepto_1"
    default_emi:str = "concepto_9"
    
    class Transac(TypedDict):
        origen_id:str
        num_cuenta:str
        # oficina:int
        divisa:str
        # fecha_operacion:datetime
        # fecha_valor:NotRequired[datetime]
        fecha_transaccion:NotRequired[datetime]
        importe:float
        saldo:float
        concepto_comun:str
        concepto_propio:str
        # ref_1:str
        referencia:str
        # concepto_1:NotRequired[str]
        destinatario:str # concepto 1 o 9
        emisor:str # concepto 1 o 9
        descripcion:NotRequired[str] # concepto 5
        descripcion_ext:NotRequired[str] #concepto 7
        cod_oper_tarjeta:NotRequired[str] # concepto 9
        # concepto_2:NotRequired[str]
        # concepto_3:NotRequired[str]
        # concepto_4:NotRequired[str]
        # concepto_5:NotRequired[str]
        # concepto_6:NotRequired[str]
        # concepto_7:NotRequired[str]
        # concepto_8:NotRequired[str]
        # concepto_9:NotRequired[str]
        # concepto_10:NotRequired[str]
    
    @classmethod
    def normalize_str(cls, cadena:str):
        #Trim espacios y caracteres de mierda
        normalized:str = cadena.strip(' \t\n\r')
        #Trim de espacios redundantes
        normalized = re.sub(r"\s{2,}"," ",normalized)
        #Puntos y comas por espacios
        normalized = normalized.replace(";", " ")
        return normalized
    
    @classmethod
    def getLocalTime(cls,date_str:str)->datetime:
        local_time:datetime = datetime.now()
        try:
            europeTZ = timezone("Europe/Madrid")
            date_date = datetime.strptime(date_str.replace("-","/"),f"%d/%m/%Y")
            local_time =  utc.localize(date_date).astimezone(europeTZ)
        except Exception as err:
            print(err.args[0])
        return local_time

    
    @classmethod
    def getFechaTransaccion(cls,concepto:str, default:str = "")->datetime:
        fecha_date = None
        try:
            literal_str = "Fecha de operación: "
            #14-12-2025
            fecha = concepto[concepto.index(literal_str) + len(literal_str):concepto.index(literal_str) + len(literal_str)+10].strip()
            fecha_date = fecha
        except ValueError as err:
            print(f"Fecha transacción: {err.args[0]}")
            fecha_date = default
        return cls.getLocalTime(fecha_date)
    
    @classmethod
    def getConcepto(cls,concepto:str)->str:
        concepto_norm:str = ""
        try:
            literal_str = "Fecha de operación: "
            #14-12-2025
            concepto_norm = concepto[concepto.index(literal_str) + len(literal_str)+11:].strip()
        except ValueError:
            concepto_norm = concepto
        return concepto_norm
    
    @classmethod
    def getImporteSaldo(cls,positivo:str, negativo:str):
        res = 0
        try:
            positivo_num = locale.atof(positivo) if positivo != "" else 0
            negativo_num = -locale.atof(negativo) if negativo != "" else 0
            res = positivo_num + negativo_num
        except ValueError as err:
            print(err.args[0])
        return res
    
    @classmethod
    def getDestinatario(cls,concepto_1:str, concepto_9:str, concepto_propio:str)->str:
        dest:str = ""
        if concepto_propio in cls.concept_1_dest:
            dest = concepto_1
        elif concepto_propio in cls.concept_9_dest:
            dest = concepto_9
        else:
            dest = concepto_1 if cls.default_dest == "concepto_1" else concepto_9
        return cls.normalize_str(dest)
    
    @classmethod
    def getEmisor(cls,concepto_1:str, concepto_9:str, concepto_propio:str):
        emisor:str = ""
        if concepto_propio in cls.concept_1_dest:
            emisor= concepto_9
        elif concepto_propio in cls.concept_9_dest:
            emisor=concepto_1
        else:
            emisor=concepto_9 if cls.default_emi == "concepto_9" else concepto_1
        return cls.normalize_str(emisor)
    
    @classmethod
    def getCodTarjeta(cls,codigo:str, concepto_propio:str):
        if concepto_propio == "040":
            return cls.normalize_str(codigo)
        else:
            return ""

def cargaExcel(csvPath:Path):
    movs:list = []
    with open(csvPath, mode ='r',encoding='UTF-8') as file:    
        movs = list(csv.DictReader(file, delimiter=","))
        
    print(f"Number of transactions: {len(movs)}")
    return movs
    

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL,'')
    
    #leer transacciones
    transacs = cargaExcel(Path.home() / "Documents" / "ExpenseViewer_transactions" / "transacs_fist_load.csv")
    
    #importar
    client = MongoClient(host="localhost", port=27017)
    db = client.get_database(name="expenseTracker")
    migration_collection = db.create_collection(f"transacs_caixabank_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    # collection = db.get_collection(name="transactions")
    print(f"Cargando transacciones en {client.address}")
    result = migration_collection.insert_many(transacs)
    print(f"Carga completada: {len(result.inserted_ids)}")

    # transacs = db.get_collection(name="transactions")
    transacs_norm = db.get_collection(name="transactions")
    deleted= transacs_norm.delete_many(filter={})
    print(f"Tabla principal reseteada. Deleted count: {deleted.deleted_count}")
    print(f"Conectado a {client.address}/{db.name} leyendo {migration_collection.name}")
    
    id_normalized = list(map(lambda transac: ObjectId(transac.get("origen_id")), 
                        transacs_norm.find(filter = {}, projection={"origen_id":1, "_id":0})))
    
    print(id_normalized)
    transacs_not_norm = migration_collection.find(filter={"$and":[
        {"_id":{"$not":{"$in":id_normalized}}},
        # {"_id":{"$eq":ObjectId("694fa42c9ca3235ae089983e")}}
        ]})
    print("Lectura completada")
    
    normalizer = TransacNormalization()
    
    for transac in migration_collection.find(filter={}):
        try:
            comple_9 = transac.get("Concepto complementario 9")
            comple_1 = normalizer.getConcepto(transac.get("Concepto complementario 1"))
            concepto_propio = transac.get("Concepto propio")
            fecha_transac = normalizer.getFechaTransaccion(transac.get("Concepto complementario 1"),transac.get("F. Operaci\u00f3n"))
            
            print("\n --> Nueva transacción:")
            new_transac = normalizer.Transac(origen_id=str(transac.get("_id","")),
                                num_cuenta=transac.get("\ufeffN\u00famero de cuenta"),
                                # oficina=transac.get("Oficina"),
                                divisa=transac.get("Divisa"),
                                # fecha_valor=normalizer.getLocalTime(transac.get("F. Valor")),
                                fecha_transaccion=fecha_transac,
                                importe=normalizer.getImporteSaldo(transac.get("Ingreso (+)"),transac.get("Gasto (-)")),
                                saldo=normalizer.getImporteSaldo(transac.get("Saldo (+)"),transac.get("Saldo (-)")),
                                concepto_comun=transac.get("Concepto com\u00fan"),
                                concepto_propio=concepto_propio,
                                # ref_1=transac.get("Referencia 1"),
                                referencia=normalizer.normalize_str(transac.get("Referencia 2")),
                                destinatario=normalizer.getDestinatario(comple_1, comple_9, concepto_propio), # concepto 1 o 9
                                emisor=normalizer.getEmisor(comple_1, comple_9, concepto_propio), # concepto 1 o 9
                                descripcion=normalizer.normalize_str(transac.get("Concepto complementario 5")),
                                descripcion_ext=normalizer.normalize_str(transac.get("Concepto complementario 7")), #concepto 7
                                cod_oper_tarjeta=normalizer.getCodTarjeta(comple_9,concepto_propio) # concepto 9
                                )
            
            #TODO: EMISOR/DESTINATARIO VACIOS --> autocompletar usuario propietario cuenta
            print(new_transac)
            transacs_norm.insert_one(new_transac)
        except DuplicateKeyError as err:
            print(f"!!! ERROR Clave duplicada: {err.details.get("errmsg")}") # type: ignore
            break