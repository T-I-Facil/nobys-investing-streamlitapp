from pydantic import BaseModel, validator
import re
from datetime import datetime
from pycpfcnpj import cpfcnpj

class InvoiceInput(BaseModel):
    nome: str
    cpf: str
    valor_inicial_nota: float
    data_operacao: datetime
    nota_fiscal: str	
    nome_empresa: str
    juros: float
    valor_emprestado: float	
    dias_adiantados: int
    data_registro: datetime = datetime.now()
    valor_final_da_nota: float
    data_recebimento: datetime
    approved: bool = False
    juros_em_reais: float
    
    @validator("cpf")
    def validate_cpf(cls, value):
        cpf = re.sub(r"[^0-9]", "", value)
        if not cpfcnpj.validate(cpf):
            raise ValueError(f"O CNPJ ou CPF informado está inválido.")

        return cpf
