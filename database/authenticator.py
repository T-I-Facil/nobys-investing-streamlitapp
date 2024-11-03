
from pymongo import MongoClient
from config.environments import Environment

class AuthenticatorRepository:
    def __init__(self):
        self.client = MongoClient(Environment().MONGO_DB)
        self.db = self.client["Nobys-invest"]

    def get_user(self, username, password):
        user = self.db["users"].find_one({"username": username, "password": password})
        print(user)