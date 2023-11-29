import streamlit as st
from .components import table


def render():
    st.markdown(body="# Administrate campaigns")
    st.divider()

    table.render()
