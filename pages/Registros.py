import streamlit as st
from database.db_handler import DbHandler

st.set_page_config(page_title="Registros", layout="centered", page_icon="assets/nobys_logo.png")
db_handler = DbHandler()

edited_df = st.data_editor(
    db_handler.get_db, 
    hide_index=True, 
    use_container_width=True, 
    num_rows='dynamic',
    column_config={
        "data_operacao": st.column_config.DateColumn("Data da Operação", format="DD/MM/YYYY", required=True),
        "valor_inicial_nota": st.column_config.NumberColumn("Valor da Nota", format="%.2f", required=True),
        "nota_fiscal": st.column_config.TextColumn("Nº Nota Fiscal", required=True),
        "valor_emprestado": st.column_config.NumberColumn("Valor Emprestado", format="%.2f", required=True),
        "dias_adiantados": st.column_config.NumberColumn("Dias Adiantados", format="%.0f", required=True),
        "juros": st.column_config.NumberColumn("Juros", format="%.2f", required=True),
        "nome": st.column_config.TextColumn("Cliente", required=True),
    }
)

edited_df.to_excel("database/database.xlsx", index=False)