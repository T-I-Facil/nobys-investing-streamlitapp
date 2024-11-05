import streamlit as st
import pandas as pd

def delete_session():
    for key in st.session_state.keys():
        if type(st.session_state[key]) == type(pd.DataFrame()):
            del st.session_state[key]