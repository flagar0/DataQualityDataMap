import streamlit as st
from .components import table


def render():
    st.markdown(body="# Create a new campaign")
    st.divider()

    table.render()
