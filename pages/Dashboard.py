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
df["juros_em_reais"] =  df["valor_inicial_nota"] - df['valor_final_da_nota']

# Soma todos os valores de juros em reais para obter o total
total_juros_arrecadados = df["juros_em_reais"].sum()

m1, m2, m3 = st.columns(3)

m1.metric(label="Total de Notas", value=f"{df.shape[0]:,.0f}".replace(".", ","))
m2.metric(label="Total de Juros", value=f"R$ {total_juros_arrecadados:,.2f}".replace(".", ","))
m3.metric(label="Total de Notas em R$", value=f"R$ {df['valor_inicial_nota'].sum():,.0f}".replace(",", "."))

df_grouped_sum = df.groupby("data_operacao").sum(numeric_only=True).reset_index().sort_values(by="data_operacao")
df_grouped_mean = df.groupby("data_operacao").mean(numeric_only=True).reset_index().sort_values(by="data_operacao")

fig = px.line(df_grouped_sum, x='data_operacao', y=['valor_emprestado', 'juros'], title='Valor Emprestado e Juros ao Longo do Tempo')
st.plotly_chart(fig)

fig = px.line(df_grouped_sum, x='data_operacao', y='valor_inicial_nota', title='Total de Notas por Data')
st.plotly_chart(fig)

fig = px.line(df_grouped_mean, x='data_operacao', y='juros_em_reais', title='Média de Juros por Data')
st.plotly_chart(fig)
