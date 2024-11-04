import streamlit as st
from database.invoice import InvoiceRepository
import plotly.express as px
from session.load_session import load_session
from components.sidebar_filters import get_periods_filters
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(page_title="Dashboard", layout="wide", page_icon="assets/nobys_logo.png")
st.sidebar.image("assets/nobys_banner.png")
db_handler = InvoiceRepository()

style_metric_cards(border_radius_px=20)

load_session()
get_periods_filters()

if not st.session_state.logged_in:
    st.error("Login inválido. Por favor, realize o login novamente.")
    st.stop()

df = db_handler.get_invoices_df(st.session_state.period)
# Calcula o valor dos juros para cada linha
df["juros_em_reais"] = df["juros"] * df["valor_inicial_nota"]

# Soma todos os valores de juros em reais para obter o total
total_juros_arrecadados = df["juros_em_reais"].sum()


m1, m2, m3 = st.columns(3)

m1.metric(label="Total de Notas", value=f"{df.shape[0]:,.0f}".replace(".", ","))

m2.metric(label="Total de Juros Arrecadados", value=f"R$ {total_juros_arrecadados:,.2f}".replace(".", ","))

m3.metric(label="Total Arrecadado", value=f"R$ {df['valor_emprestado'].sum():,.0f}".replace(",", "."))

fig = px.bar(df, x='nome', y='valor_emprestado', title='Valor Emprestado por Pessoa')
st.plotly_chart(fig)

fig = px.bar(df, x='nome', y='juros', title='Juros por Pessoa')
st.plotly_chart(fig)

fig = px.line(df, x='data_operacao', y=['valor_emprestado', 'juros'], title='Valor Emprestado e Juros ao Longo do Tempo')
st.plotly_chart(fig)

fig = px.scatter(df, x='valor_inicial_nota', y='juros', color='nome', title='Valor Inicial da Nota vs Juros')
st.plotly_chart(fig)
