import streamlit as st
from .components import form


def render():
    st.markdown(body="# Login")
    st.divider()

    form.render()
