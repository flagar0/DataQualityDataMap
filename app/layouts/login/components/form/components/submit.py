import streamlit as st
from config.auth import Auth


def exec():
    auth: Auth = st.session_state.auth
    auth.is_authenticated = True
    auth.user = st.session_state["auth_email_input"]

    st.success(body="Sucessfull Logged")
