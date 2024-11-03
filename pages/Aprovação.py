import streamlit as st  
from database.invoice import InvoiceRepository
import pandas as pd

st.set_page_config(page_title="Aprovação", layout="centered", page_icon="assets/nobys_logo.png")
db_handler = InvoiceRepository()