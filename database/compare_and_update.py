import pandas as pd
import numpy as np
from pandas._libs.tslibs.timestamps import Timestamp
from database.invoice import InvoiceRepository

def format_param(param):
    if type(param) is bool:
        return param

    if type(param) is np.int64 or type(param) is np.float64:
        return param
    
    if type(param) is np.bool_:
        return bool(param)

    if type(param) is int or type(param) is float:
        return param

    if isinstance(param, Timestamp):
        return param.date().strftime("%d-%m-%Y")

    return {"True": True, "False": False}.get(param, param.upper())

def format_key(key):
    return {
        "Data da Operação": "data_operacao",
        "Valor Emprestado": "valor_inicial_nota",
        "Nº Nota Fiscal": "nota_fiscal",
        "Valor Adiantado": "valor_emprestado",
        "Dias Adiantados": "dias_adiantados",
        "Juros": "juros",
        "Cliente": "nome",
        "CPF": "cpf",
        "Nome da Empresa": "nome_empresa",
        "Data de Recebimento": "data_recebimento",
        "Data de Registro": "data_registro",
        "Aprovado": "approved",
    }.get(key, key.lower().replace(" ", "_"))

def compare_and_update(original: pd.DataFrame, updated: pd.DataFrame, db_handler: InvoiceRepository):
    # Verifica se ambos os DataFrames têm as mesmas colunas
    original = original[updated.columns]  # Alinha as colunas do original com as do updated

    # Define '_id' como índice para ambos os DataFrames
    original.set_index("_id", inplace=True)
    updated.set_index("_id", inplace=True)
    
    # Certifica-se de que os índices estão alinhados
    original, updated = original.align(updated, join='inner', axis=0)

    # Compara os DataFrames alinhados
    alteracoes = original.compare(updated).reset_index()

    # Itera sobre as alterações e atualiza o banco de dados para cada alteração
    if len(alteracoes) > 0:
        _id = alteracoes["_id"].iloc[0]
        key = alteracoes.columns[1][0]  # Nome da coluna alterada
        value = alteracoes[key]["other"].iloc[0]  # Novo valor na coluna alterada
        
        # Prepara os parâmetros de atualização
        update_field = format_key(key)
        update_value = format_param(value)
        
        # Realiza a atualização no MongoDB
        db_handler.update_invoice(_id, update_field, update_value)

        print(f"Updated {_id}: {update_field} -> {update_value}")

