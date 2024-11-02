import streamlit as st


def get_input_form():
    FORMULARIO = {
        "nome": st.text_input("Cliente"),
        "cpf": st.text_input("CPF", max_chars=11),
        "valor_inicial_nota": st.number_input("Valor da Nota"),
        "nota_fiscal": st.text_input("Nº Nota Fiscal"),
        "nome_empresa": st.text_input("Nome da Empresa"),
        "data_operacao": st.date_input("Data da Operação", format="DD/MM/YYYY"),
        "valor_emprestado": st.number_input("Valor Emprestado"),
        "dias_adiantados": st.number_input("Dias Adiantados", format="%.0f")
    }

    return FORMULARIO