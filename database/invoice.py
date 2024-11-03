from pymongo import MongoClient
from config.environments import Environment
from .models.invoice_input import InvoiceInput
import pandas as pd
from datetime import timedelta

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

        if filters.get("data_registro"):
            start_of_day = filters["data_registro"].replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            query_filters["data_registro"] = {"$gte": start_of_day, "$lt": end_of_day}


        query_filters = {k: v for k, v in query_filters.items() if v is not None}

        return self.db["invoices"].find(query_filters)


    
    def get_invoices_df(self, filters):
        filters = {k: v for k, v in filters.items() if v not in (None, '', [])}

        return pd.DataFrame(self.get_invoices(filters)).drop("_id", axis=1)
    
    def delete_invoice(self, invoice: str):
        self.db["invoices"].delete_one({"nota_fiscal": invoice})

    def approve_invoice(self, invoice: str):
        self.db["invoices"].update_one({"nota_fiscal": invoice}, {"$set": {"approved": True}})