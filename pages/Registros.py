import streamlit as st
from database.invoice import InvoiceRepository
from components.sidebar_filters import get_sidebar_filters
from session.load_session import load_session

st.set_page_config(page_title="Registros", layout="centered", page_icon="assets/nobys_logo.png")
db_handler = InvoiceRepository()

load_session()

get_sidebar_filters()

df = db_handler.get_invoices_df(st.session_state.filters)

edited_df = st.dataframe(
    data=df, 
    hide_index=True, 
    use_container_width=True, 
    column_config={
        "data_operacao": st.column_config.DateColumn("Data da Operação", format="DD/MM/YYYY", required=True),
        "valor_inicial_nota": st.column_config.NumberColumn("Valor da Nota", format="R$ %.2f", required=True),
        "nota_fiscal": st.column_config.TextColumn("Nº Nota Fiscal", required=True),
        "valor_emprestado": st.column_config.NumberColumn("Valor Emprestado", format="R$ %.2f", required=True),
        "dias_adiantados": st.column_config.NumberColumn("Dias Adiantados", format="%.0f", required=True),
        "juros": st.column_config.NumberColumn("Juros", format="%.2f%%", required=True),
        "nome": st.column_config.TextColumn("Cliente", required=True),
        "cpf": st.column_config.TextColumn("CPF", required=True),
        "nome_empresa": st.column_config.TextColumn("Nome da Empresa", required=True),
        "data_recebimento": st.column_config.DateColumn("Data de Recebimento", format="DD/MM/YYYY", required=True),
        "valor_final_da_nota": st.column_config.NumberColumn("Valor Final da Nota", format="R$ %.2f", required=True),
        "data_registro": st.column_config.DateColumn("Data de Registro", format="DD/MM/YYYY", required=True),
    }
)

# adiciona um filtro para o dataframe, se elet iver vazio, retorna uma mensagem de erro dizendo que não encontrou porra nenhuma nota fiscal
if len(df) == 0:
    st.error("Nenhuma nota fiscal encontrada.")

else:
    with st.expander("Deletar Registro"):
        invoice = st.selectbox("Selecione a Nota Fiscal:", df["nota_fiscal"])
        submit = st.button("Deletar")
        if submit:
            db_handler.delete_invoice(invoice)
