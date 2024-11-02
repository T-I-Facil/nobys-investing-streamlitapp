import streamlit as st

def load_session():
    if "filters" not in st.session_state:
        st.session_state.filters = {}