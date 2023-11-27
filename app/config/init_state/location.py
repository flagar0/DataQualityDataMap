import streamlit as st

def init ():
    if "table_data" not in st.session_state:
        st.session_state.table_data = []