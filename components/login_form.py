import streamlit as st


def get_login_form():
    FORMULARIO = {
        "email": st.text_input("Email"),
        "password": st.text_input("Password", type="password"),
    }

    return FORMULARIO