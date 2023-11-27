import streamlit as st


def exec():
    flag_required = []
    if (
        st.session_state["auth_email_input"] is None
        and st.session_state["auth_email_input"] == ""
    ):
        flag_required.append("User E-mail")

    if (
        st.session_state["auth_pwd_input"] is None
        and st.session_state["auth_pwd_input"] == ""
    ):
        flag_required.append("Password")

    if flag_required:
        st.error(body=f"Required fields missing: {flag_required}")
        return False
