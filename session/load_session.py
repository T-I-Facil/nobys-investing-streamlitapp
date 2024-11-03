import streamlit as st

def load_session():
    if "filters" not in st.session_state:
        st.session_state.filters = {}

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False