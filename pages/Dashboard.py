import streamlit as st
from database.invoice import InvoiceRepository
import plotly.express as px
from session.load_session import load_session

st.set_page_config(page_title="Dashboard", layout="wide", page_icon="assets/nobys_logo.png")
st.sidebar.image("assets/nobys_banner.png")
db_handler = InvoiceRepository()

load_session()

if not st.session_state.logged_in:
    st.error("Login inválido. Por favor, realize o login novamente.")
    st.stop()

df = db_handler.get_invoices_df(st.session_state.filters)
df = db_handler.get_invoices_df(st.session_state.filters)

fig = px.bar(df, x='nome', y='valor_emprestado', title='Valor Emprestado por Pessoa')
st.plotly_chart(fig)

fig = px.bar(df, x='nome', y='juros', title='Juros por Pessoa')
st.plotly_chart(fig)

fig = px.line(df, x='data_operacao', y=['valor_emprestado', 'juros'], title='Valor Emprestado e Juros ao Longo do Tempo')
st.plotly_chart(fig)

fig = px.scatter(df, x='valor_inicial_nota', y='juros', color='nome', title='Valor Inicial da Nota vs Juros')
st.plotly_chart(fig)
