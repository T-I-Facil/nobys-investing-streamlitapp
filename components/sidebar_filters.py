from datetime import datetime, timedelta
import streamlit as st
from session.delete_session import delete_session

def get_sidebar_filters():
    with st.sidebar:
        form = st.form("Formulário", clear_on_submit=True)
        
        # Definindo o valor padrão de data_registro_inicial para 10 dias antes do dia atual
        default_data_inicial = datetime.now().date() - timedelta(days=10)
        
        cpf = form.text_input("CPF", max_chars=11)
        nome = form.text_input("Nome")
        data_registro_inicial = form.date_input("Data de Registro Inicial", value=default_data_inicial, format="DD/MM/YYYY")
        data_registro_final = form.date_input("Data de Registro Final", format="DD/MM/YYYY")
        nota_fiscal = form.text_input("Nº Nota Fiscal")

        c1, c2, _ = form.columns(3)
        clear = c1.form_submit_button("Limpar")
        apply = c2.form_submit_button("Aplicar")

        if clear:
            st.session_state.filters = {}
            delete_session()

        if apply:
            st.session_state.filters = {
                "cpf": cpf,
                "nome": nome,
                "data_registro_inicial": datetime.combine(data_registro_inicial, datetime.min.time()),
                "data_registro_final": datetime.combine(data_registro_final, datetime.max.time()),
                "nota_fiscal": nota_fiscal
            }
            delete_session()

def get_periods_filters():
    default_data_inicial = datetime.now().date() - timedelta(days=10)

    with st.sidebar:
        data_registro_inicial = st.date_input("Data de Registro Inicial", value=default_data_inicial, format="DD/MM/YYYY")
        data_registro_final = st.date_input("Data de Registro Final", format="DD/MM/YYYY")

    st.session_state.period = {
        "data_registro_inicial": datetime.combine(data_registro_inicial, datetime.min.time()),
        "data_registro_final": datetime.combine(data_registro_final, datetime.max.time()),
    }

