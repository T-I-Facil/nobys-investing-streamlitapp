import streamlit as st
from datetime import datetime

def get_sidebar_filters():
    with st.sidebar:
        form = st.form("Formulário")
        cpf = form.text_input("CPF", max_chars=11)
        nome = form.text_input("Nome")
        data_registro = form.date_input("Data de Registro", format="DD/MM/YYYY")
        nota_fiscal = form.text_input("Nº Nota Fiscal")   

        c1, c2, _ = form.columns(3)
        clear = c1.form_submit_button("Clear")
        apply = c2.form_submit_button("Apply")

        if clear:
            st.session_state.filters = {}

        if apply:
            st.session_state.filters = {
                "cpf": cpf,
                "nome": nome,
                "data_registro": datetime.combine(data_registro, datetime.min.time()),
                "nota_fiscal": nota_fiscal
            }