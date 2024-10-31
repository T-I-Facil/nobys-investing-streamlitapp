import streamlit as st


def get_input_form():
    FORMULARIO = {
        "nome":  st.text_input("sua mãe?"),
        "valor_inicial_nota": st.number_input("nota fiscal?"),
        "nota_fiscal": st.text_input("nota fiscal?"),
        "data_operacao": st.date_input("data da operação"),
        "valor_emprestado": st.number_input("valor emprestado"),
        "dias_adiantados": st.number_input("dias adiantados")
    }
    return FORMULARIO