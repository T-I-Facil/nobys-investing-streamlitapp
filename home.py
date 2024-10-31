from database.db_handler import DbHandler
from database.models.input_data import InputData
import streamlit as st
from components.input_form import get_input_form

db_handler = DbHandler()

with st.form("Formulário"):
    input_data = get_input_form()
    submit = st.form_submit_button("Enviar")
    juros = 0.229
    dias_adiantados = input_data['dias_adiantados']
    if dias_adiantados > 7:
        juros = dias_adiantados*(0.98/30)

    if submit:
        input_data_atualizado = {**input_data, "juros": 0.07}
        input_data = InputData(**input_data_atualizado)
        print(input_data)
        db_handler.write_new_data(input_data)

search_name = st.text_input("qual nome você quer pesquisar?")
filter_date = st.date_input("qual data você quer filtrar?")
result = db_handler.search_by_name(search_name)
result = db_handler.search_by_date(filter_date)
st.dataframe(result)
# db_handler.write_new_data(input_data)