import streamlit as st
from .components import table


def render():
    st.markdown(body="# View Public campaigns")
    st.divider()

    table.render()
