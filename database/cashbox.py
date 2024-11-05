from pymongo import MongoClient
from config.environments import Environment
from .models.cashbox import CashBox, Transaction
import pandas as pd

class CashboxRepository:
    def __init__(self):
        self.client = MongoClient(Environment().MONGO_DB)
        self.db = self.client["Nobys-invest"]
        self.cashbox = self.db["cashbox"]
        self.transactions = self.db["transactions"]


    def add_transaction(self, transaction_data: dict):
        # Validando e criando a transação
        transaction = Transaction(**transaction_data)

        # Obtém o saldo atual do caixa
        cashbox_data = self.cashbox.find_one()
        current_balance = cashbox_data["balance"] if cashbox_data else 0.0

        # Calcula o saldo atualizado para a transação atual
        transaction.apply_transaction(current_balance)

        # Insere a transação no histórico com o saldo atualizado
        self.transactions.insert_one(transaction.model_dump(by_alias=True))

        # Atualiza o saldo do caixa com o novo saldo calculado
        if cashbox_data:
            # Atualiza o saldo do caixa existente
            self.cashbox.update_one(
                {"_id": cashbox_data["_id"]},
                {"$set": {"balance": transaction.balance}}
            )
        else:
            # Cria um novo documento para o caixa se ele não existir
            self.cashbox.insert_one({"balance": transaction.balance})

        return transaction


    def get_transactions(self):
        df = pd.DataFrame(self.transactions.find())
        if df.empty:
            return pd.DataFrame()
        return pd.DataFrame(self.transactions.find()).drop("_id", axis=1)
    
    def get_balance(self):
        cashbox_data = self.cashbox.find_one()
        return cashbox_data["balance"] if cashbox_data else 0.0