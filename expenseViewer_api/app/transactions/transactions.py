from app.db import get_transac_por_concepto, get_balance, get_transacs
from babel import numbers
from bson import ObjectId
from logging import Logger,getLogger
import pprint
from datetime import datetime


class Transaction:
    logger:Logger = getLogger(__name__)
    
    currency_dict = {
        "EUR":"€",
        "GBP":"£",
        "DOL":"$"
    }
    
    @classmethod
    def __format_money(cls, cash:float, currency:str)->str:
        cur_formated = cls.currency_dict.get(currency)
        formated_money = numbers.format_decimal(cash, locale="es_ES")
        return f"{formated_money} {cur_formated}"

    
    @classmethod
    def balance(cls):
        balance_dict = {}
        try:
            balance_dict=get_balance()
        except Exception:
            balance_dict= {"divisa": "EUR","saldo":0}
            
        return {"money":cls.__format_money(balance_dict.get('saldo', ''),
                                  balance_dict.get('divisa','DOL'))}
        
    @classmethod
    def get_transacs(cls, concepto:str):
        return get_transac_por_concepto(concepto)
    
    @classmethod
    def get_transacs_last_30(cls):       
        cls.logger.info("Peticion transacciones") 
        transacs_form = list(
            map(lambda transac: {
                 "_id":str(transac.get("_id", "")), 
                 "account": transac.get("num_cuenta", ""),
                 "transac_date": datetime.strftime(transac.get("fecha_transaccion", ""), f"%d/%m/%Y"),
                 "amount": cls.__format_money(transac.get("importe", 0), transac.get("divisa","")) ,
                 "balance": transac.get("saldo", 0),
                 "reference": transac.get("referencia",""),
                 "dest": transac.get("destinatario_1",""),
                 "issuer": transac.get("emisor", ""),
                 "description": transac.get("desc_usuario",""),
                 "concept": transac.get("desc_concepto_compuesto","")
                }, get_transacs())
            )
        pprint.pprint(transacs_form[0])
        return transacs_form