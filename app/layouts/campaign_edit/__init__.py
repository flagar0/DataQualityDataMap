import streamlit as st
from .components import table


def render():
    st.markdown(body="# Edit campaigns")
    st.divider()

    table.render()
