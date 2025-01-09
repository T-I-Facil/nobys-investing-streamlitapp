from pymongo import MongoClient
from config.environments import Environment
from .models.invoice_input import InvoiceInput
import pandas as pd
from bson import ObjectId

class InvoiceRepository:
    def __init__(self):
        self.client = MongoClient(Environment().MONGO_DB)
        self.db = self.client["Nobys-invest"]

    def insert_invoice(self, invoice: InvoiceInput):
        self.db["invoices"].insert_one(invoice.model_dump())

    def get_invoices(self, filters):
        query_filters = {
            "cpf": filters.get("cpf"),
            "nome": {"$regex": filters.get("nome"), "$options": "i"} if filters.get("nome") else None,
            "nota_fiscal": filters.get("nota_fiscal"),
        }

        if filters.get("data_registro_inicial") and filters.get("data_registro_final"):
            start_of_day = filters["data_registro_inicial"].replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = filters["data_registro_final"].replace(hour=23, minute=59, second=59, microsecond=999999)
            query_filters["data_registro"] = {"$gte": start_of_day, "$lte": end_of_day}


        query_filters = {k: v for k, v in query_filters.items() if v is not None}

        return self.db["invoices"].find(query_filters)

    def update_invoice(self, _id, key, value):
       _id = ObjectId(_id)
       self.db["invoices"].update_one({"_id": _id}, {"$set": {key: value}})

    def get_invoices_df(self, filters):
        filters = {k: v for k, v in filters.items() if v not in (None, '', [])}

        df = pd.DataFrame(self.get_invoices(filters))
        if len(df) == 0:
            return pd.DataFrame()
        
        return df[[
            "nome", 
            "cpf", 
            "nome_empresa",
            "approved", 
            "valor_emprestado",
            "data_recebimento", 
            "data_registro", 
            "data_operacao", 
            "valor_inicial_nota", 
            "juros", 
            "juros_em_reais",
            "dias_adiantados", 
            "nota_fiscal", 
            "_id"
        ]]
    
    def delete_invoice(self, invoice: str):
        self.db["invoices"].delete_one({"nota_fiscal": invoice})

    def approve_invoice(self, invoice: str):
        self.db["invoices"].update_one({"nota_fiscal": invoice}, {"$set": {"approved": True}})