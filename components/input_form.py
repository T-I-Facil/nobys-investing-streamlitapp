import streamlit as st


def get_input_form():
    FORMULARIO = {
        "nome":  st.text_input("Cliente"),
        "valor_inicial_nota": st.number_input("Valor da Nota"),
        "nota_fiscal": st.text_input("Nº Nota Fiscal"),
        "data_operacao": st.date_input("Data da Operação", format="DD/MM/YYYY"),
        "valor_emprestado": st.number_input("Valor Emprestado"),
        "dias_adiantados": st.number_input("Dias Adiantados", format="%.0f")
    }

    return FORMULARIO