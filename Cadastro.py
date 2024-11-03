from database.models.invoice_input import InvoiceInput
import streamlit as st
from components.input_form import get_input_form
from database.invoice import InvoiceRepository
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_authenticator import Authenticate
from datetime import timedelta

invoice_repository = InvoiceRepository()

st.set_page_config(page_title="Nobys", layout="centered", page_icon="assets/nobys_logo.png")
style_metric_cards(border_radius_px=20)

st.sidebar.image("assets/nobys_banner.png")
juros_simulado = (0.098/30)*7
c1, c2 = st.columns(2)
m1, m2, m3 = st.columns(3)

valor_nota_simulado = c1.number_input("Valor da Nota", step=0.5)
dias_adiantados_simulado = c2.number_input("Dias Adiantados", step=1)

if dias_adiantados_simulado > 7:
    juros_simulado = (0.098/30)*dias_adiantados_simulado

juros_final = juros_simulado*valor_nota_simulado
juros_string = juros_simulado*100
m1.metric(label="Juros", value=f"{juros_string:,.2f}%".replace(".", ","))
m2.metric(label="Valor Final:", value=f"R$ {valor_nota_simulado-juros_final:,.2f}".replace(".", ","))
m3.metric(label="Valor Juros", value=f"R$ {juros_final:,.2f}".replace(".", ","))

with st.form("Formulário"):
    input_data = get_input_form()
    submit = st.form_submit_button("Enviar")

    dias_adiantados = input_data['dias_adiantados']
    valor_nota = input_data['valor_inicial_nota']

    data_recebimento = input_data['data_operacao'] + timedelta(days=dias_adiantados)

    juros = (0.098/30)*7
    if dias_adiantados > 7:
        juros = (0.098/30)*dias_adiantados

    if submit:
        input_data_atualizado = {
            **input_data, 
            "juros": juros, 
            "valor_final_da_nota": valor_nota-juros, 
            "data_recebimento": data_recebimento
            }
        
        input_data = InvoiceInput(**input_data_atualizado)
        invoice_repository.insert_invoice(input_data)
        st.success("Dados inseridos com sucesso!")
