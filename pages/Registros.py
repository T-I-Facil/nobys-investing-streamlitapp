import streamlit as st
from database.invoice import InvoiceRepository
from database.compare_and_update import compare_and_update
from components.sidebar_filters import get_sidebar_filters
from components.expanders import get_expanders
from components.panel import get_invoices_panel
from session.load_session import load_session

st.set_page_config(page_title="Registros", layout="centered", page_icon="assets/nobys_logo.png")
st.sidebar.image("assets/nobys_banner.png")
db_handler = InvoiceRepository()

load_session()

if not st.session_state.logged_in:
    st.error("Login inválido. Por favor, realize o login novamente.")
    st.stop()

get_sidebar_filters()

if "invoices" not in st.session_state:
    # Faz o request das vendas de determinado período. Os dados são inseridos numa variável dentro
    # de st.session_state. Essa variável pode ser acessada globalmente. Essa função só será executada
    # uma vez por período selecionado e uma vez que a variável de sessão é criada. O seu valor é CONSTANTE.
    # Sempre que um filtro é adicionado ou o período é alterado, a sessão é deletada e um novo request
    # é feito.
    st.session_state.invoices = db_handler.get_invoices_df(st.session_state.filters)

    if not st.session_state.is_admin:
        st.session_state.invoices.drop("approved", axis=1, inplace=True)

if "value_invoices" not in st.session_state:
    # Inicializa a variável de sessão "value" caso ela não exista. Por padrão, o value será o dataframe
    # das vendas original. Sempre que uma alteração é feita no painel, o dataframe do painel é comparado
    # com o dataframe de "value" e o dataframe alterado é inserido em seu lugar.
    st.session_state.value_invoices = st.session_state.invoices
    

get_invoices_panel(st.session_state.invoices)
get_expanders(db_handler)

if (
    st.session_state.panel_invoices is not None
    and not st.session_state.panel_invoices.equals(st.session_state["value_invoices"])
):
    # Compara o dataframe do painel com o dataframe de value e faz um request da diferença entre os
    # dataframes, caso ela exista.
    compare_and_update(
        st.session_state["value_invoices"].copy(),
        st.session_state.panel_invoices.copy(),
        db_handler.db["invoices"],
    )

    # Após o request ser feito, o valor de value é alterado pelo valor após a alteração do dataframe.
    st.session_state["value_invoices"] = st.session_state.panel_invoices