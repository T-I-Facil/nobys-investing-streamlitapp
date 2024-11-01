import pandas as pd
from .models.input_data import InputData
from datetime import datetime

class DbHandler:
    def __init__(self):
        self.db: pd.DataFrame = pd.read_excel("database/database.xlsx")
        self.db['data_operacao'] = pd.to_datetime(self.db['data_operacao'])

    def write_new_data(self, input_data: InputData):
        new_line = pd.DataFrame([input_data.dict()])
        self.db = pd.concat([self.db, new_line])
        self.db.to_excel("database/database.xlsx", index=False)

    def search_by_name(self, name: str): 
        result = self.db[self.db['nome'].str.contains(name, case=False, na=False)]
        return result

    def search_by_date(self, date: datetime):
        result = self.db[self.db['data_operacao'].dt.date == date]
        return result

    @property
    def get_db(self):
        return self.db