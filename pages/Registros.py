import streamlit as st
from database.invoice import InvoiceRepository
from database.compare_and_update import compare_and_update
from components.sidebar_filters import get_sidebar_filters
from components.expanders import get_expanders
from components.panel import get_invoices_panel
from session.load_session import load_session
from database.cashbox import CashboxRepository
import plotly.express as px
from session.delete_session import delete_session

st.set_page_config(page_title="Registros", layout="wide", page_icon="assets/nobys_logo.png")
st.sidebar.image("assets/nobys_banner.png")
invoice = InvoiceRepository()
cashbox = CashboxRepository()

load_session()

if not st.session_state.logged_in:
    st.error("Login inválido. Por favor, realize o login novamente.")
    st.stop()

update = st.sidebar.button("Atualizar Dados")
if update:
    delete_session()
    st.rerun()

get_sidebar_filters()

if "invoices" not in st.session_state:
    # Faz o request das vendas de determinado período. Os dados são inseridos numa variável dentro
    # de st.session_state. Essa variável pode ser acessada globalmente. Essa função só será executada
    # uma vez por período selecionado e uma vez que a variável de sessão é criada. O seu valor é CONSTANTE.
    # Sempre que um filtro é adicionado ou o período é alterado, a sessão é deletada e um novo request
    # é feito.
    st.session_state.invoices = invoice.get_invoices_df(st.session_state.filters)

    if not st.session_state.is_admin and len(st.session_state.invoices) > 0:
        st.session_state.invoices.drop("approved", axis=1, inplace=True)

if "value_invoices" not in st.session_state:
    # Inicializa a variável de sessão "value" caso ela não exista. Por padrão, o value será o dataframe
    # das vendas original. Sempre que uma alteração é feita no painel, o dataframe do painel é comparado
    # com o dataframe de "value" e o dataframe alterado é inserido em seu lugar.
    st.session_state.value_invoices = st.session_state.invoices
    
if len(st.session_state.invoices) == 0:
    st.error("Nenhuma nota fiscal encontrada.")
    st.stop()

get_invoices_panel(st.session_state.invoices)
get_expanders(invoice)

if (
    st.session_state.panel_invoices is not None
    and not st.session_state.panel_invoices.equals(st.session_state["value_invoices"])
):
    # Compara o dataframe do painel com o dataframe de value e faz um request da diferença entre os
    # dataframes, caso ela exista.
    compare_and_update(
        st.session_state["value_invoices"].copy(),
        st.session_state.panel_invoices.copy(),
        invoice,
    )

    # Após o request ser feito, o valor de value é alterado pelo valor após a alteração do dataframe.
    st.session_state["value_invoices"] = st.session_state.panel_invoices

transactions = cashbox.get_transactions()
with st.form("Caixa"):
    st.markdown("### Caixa")

    a1, a2, a3 = st.columns(3)

    amount = a1.number_input("Inserir Valor", step=0.5)
    tipo = a2.selectbox("Tipo", ["Entrada", "Saída"])
    description = st.text_input("Razão da Transação")

    submit = st.form_submit_button("Enviar")

    if submit:
        data = {
            "amount": amount,
            "type": tipo,
            "description": description,
            "user": st.session_state.username,
        }

        cashbox.add_transaction(data)

if len(transactions) == 0:
    st.markdown("### Nenhuma Transação Encontrada")

else:   
    with st.container():
        st.markdown(f"### Saldo: R$ {cashbox.get_balance()}")
        s1, s2 = st.columns(2)
        s2.dataframe(transactions, column_config={
            "date": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "amount": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
            "type": st.column_config.TextColumn("Tipo"),
            "description": st.column_config.TextColumn("Razão"),
            "balance": st.column_config.NumberColumn("Saldo", format="R$ %.2f"),
            "user": st.column_config.TextColumn("Usuário"),
            },
            use_container_width=True,
            hide_index=True
        )

        fig = px.line(transactions, x='date', y='balance', title='Transações')
        s1.plotly_chart(fig)