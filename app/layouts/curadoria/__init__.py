import streamlit as st
from .components import table


def render():
    st.markdown(body="# Campaigns Curation")
    st.divider()

    table.render()
