from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class Transaction(BaseModel):
    type: str  # 'entrada' ou 'saída'
    amount: float
    description: Optional[str] = None
    date: datetime = Field(default_factory=datetime.now)
    user: str
    balance: Optional[float] = None

    @validator("type")
    def validate_type(cls, value: str):
        if value.capitalize() not in {"Entrada", "Saída"}:
            raise ValueError("O tipo de transação deve ser 'entrada' ou 'saída'")
        return value.capitalize()

    @validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("O valor deve ser maior que zero")
        return value
    
    def apply_transaction(self, current_balance: float):
        """
        Calcula o novo saldo com base na transação atual.
        """
        if self.type == "Entrada":
            self.balance = current_balance + self.amount
        elif self.type == "Saída":
            self.balance = current_balance - self.amount
        return self.balance


class CashBox(BaseModel):
    balance: float
    transactions: List[Transaction] = []

    def update_balance(self, transaction: Transaction):
        if transaction.type == "Entrada":
            self.balance += transaction.amount
        elif transaction.type == "Saída":
            self.balance -= transaction.amount
        else:
            raise ValueError("Tipo de transação inválido")
