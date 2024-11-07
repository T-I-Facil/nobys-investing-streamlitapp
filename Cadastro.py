import streamlit as st
from components.login_form import get_login_form
from components.input_form import get_input_form
from database.authenticator import AuthenticatorRepository
from database.invoice import InvoiceRepository
from session.delete_session import delete_session
from session.load_session import load_session
from database.models.invoice_input import InvoiceInput
from streamlit_extras.metric_cards import style_metric_cards
from datetime import timedelta

# Configurações iniciais da página
st.set_page_config(page_title="Cadastro", layout="wide", page_icon="assets/nobys_logo.png")
style_metric_cards(border_radius_px=20)

# Inicializa repositórios e sessão
auth_repository = AuthenticatorRepository()
invoice_repository = InvoiceRepository()
load_session()

if not st.session_state.get("logged_in"):
    with st.form("login_form"):
        st.markdown("### Login")
        credentials = get_login_form()
        if st.form_submit_button("Login"):
            if auth_repository.login(credentials["email"], credentials["password"]):
                st.success("Login realizado com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Login ou senha inválidos")
else:
    # Seleção da forma de cálculo de juros
    calculo_juros = st.selectbox("Selecione a forma de calcular o juros", options=["Automático", "Manual"])
    c1, c2, c3 = st.columns(3)
    m1, m2, m3 = st.columns(3)
    valor_nota = c1.number_input("Valor da Nota", step=0.5)
    dias_adiantados = c2.number_input("Dias Adiantados", step=1)
    
    # Cálculo de juros com base na seleção
    juros_diario = 0.098 / 30
    if "Automático" in calculo_juros:
        # Juros Automático para até 7 dias de adiantamento
        juros_simulado = juros_diario * max(dias_adiantados, 7)
    elif "Manual" in calculo_juros:
        # Juros Manual: aplicando uma fórmula específica (pode ajustar conforme necessidade)
        taxa_personalizada = c3.number_input("Juros Personalizados", step=0.5)
        juros_simulado = taxa_personalizada / 100
    
    juros_percentual = juros_simulado * 100
    juros_total = juros_simulado * valor_nota
    valor_final = valor_nota - juros_total

    # Exibe métricas
    m1.metric(label="Juros", value=f"{juros_percentual:,.2f}%".replace(".", ","))
    m2.metric(label="Valor Final:", value=f"R$ {valor_final:,.2f}".replace(".", ","))
    m3.metric(label="Valor Juros", value=f"R$ {juros_total:,.2f}".replace(".", ","))

    # Cálculo do juros de acordo com a seleção no formulário
    juros_aplicado = juros_diario * max(dias_adiantados, 7)

    # Formulário para entrada de dados e envio
    with st.form("Formulário"):
        dados_input = get_input_form(calculo_juros)
        if st.form_submit_button("Enviar"):
            dias_adiantados = dados_input['dias_adiantados']
            valor_nota = dados_input['valor_inicial_nota']

            if dados_input.get('juros'):
                juros_aplicado = dados_input['juros'] / 100
            
            valor_juros = juros_aplicado * valor_nota
            dados_input_atualizado = {
                **dados_input,
                "juros": juros_aplicado * 100,
                "valor_final_da_nota": valor_nota - valor_juros,
                "data_recebimento": dados_input['data_operacao'] + timedelta(days=dias_adiantados),
                "juros_em_reais": valor_juros,
            }

            # Inserção dos dados atualizados no repositório
            invoice_data = InvoiceInput(**dados_input_atualizado)
            invoice_repository.insert_invoice(invoice_data)
            st.success("Dados inseridos com sucesso!")
            delete_session()
