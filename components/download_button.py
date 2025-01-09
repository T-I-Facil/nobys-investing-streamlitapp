import streamlit as st
import pandas as pd
import tempfile


def export_button(dataframe: pd.DataFrame):
    def download_excel():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp:
            dataframe.to_excel(temp.name)
            temp.close()

            # Ler e retornar os dados do arquivo Excel
            with open(temp.name, "rb") as f:
                data = f.read()

        return data


    st.download_button(
        "Exportar Planilha",
        download_excel(),
        file_name="registros.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )