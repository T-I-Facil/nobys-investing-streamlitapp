from pydantic import BaseModel
from datetime import datetime

class InputData(BaseModel):
    nome: str
    valor_inicial_nota: float
    data_operacao: datetime
    nota_fiscal: str	
    juros: float
    valor_emprestado: float	
    dias_adiantados: int
