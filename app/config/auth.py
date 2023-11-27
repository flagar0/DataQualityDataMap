import streamlit as st
import layouts.login


class Auth:
    def __init__(self):
        self.user = None
        self.is_authenticated = False
        self.token = None
        self.token_expire_datetime = None


def init():
    if "auth" not in st.session_state:
        st.session_state.auth = Auth()

    if not st.session_state.auth.is_authenticated:
        layouts.login.render()
        st.stop()
    else:
        with st.sidebar:
            st.markdown(body=f"**Hello {st.session_state.auth.user}**")
