
from pymongo import MongoClient
from config.environments import Environment
import streamlit as st

class AuthenticatorRepository:
    def __init__(self):
        self.client = MongoClient(Environment().MONGO_DB)
        self.db = self.client["Nobys-invest"]

    def login(self, email, password):
        user = self.db["credentials"].find_one({"email": email, "password": password})
        if not user:
            st.session_state.logged_in = False
            return

        st.session_state.username = user['login']
        st.session_state.is_admin = user["is_admin"]
        st.session_state.logged_in = True