import streamlit as st
import datetime


def render():
    st.text_input(
        key="auth_email_input",
        label="User E-mail",
    )

    st.text_input(
        key="auth_pwd_input",
        label="Password",
        type="password",
    )
