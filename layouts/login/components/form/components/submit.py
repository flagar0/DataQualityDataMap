import streamlit as st


def exec():
    st.session_state.auth.is_authenticated = True
    st.session_state.auth.user = st.session_state.auth_email_input
    st.success(body="Sucessfull Logged")
