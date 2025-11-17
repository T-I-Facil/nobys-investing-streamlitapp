from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Environment:
    def __init__(self):
        self.MONGO_DB = getenv("MONGO_DB")

        print(self.MONGO_DB)