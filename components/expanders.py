import streamlit as st

def get_expanders(db_handler):
    if len(st.session_state.invoices) == 0:
        st.error("Nenhuma nota fiscal encontrada.")

    else:
        with st.expander("Deletar Registro"):
            invoice = st.selectbox("Selecione a Nota Fiscal:", st.session_state.invoices["nota_fiscal"])
            submit = st.button("Deletar")
            if submit:
                db_handler.delete_invoice(invoice)
                