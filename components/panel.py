import streamlit as st

def get_invoices_panel(df):
    st.session_state.panel_invoices = st.data_editor(
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
            "approved": st.column_config.CheckboxColumn("Aprovado", required=True) if st.session_state.is_admin else None,
            "juros_em_reais": st.column_config.NumberColumn("Juros(R$)", format="R$ %.2f", required=True),
        },
    )