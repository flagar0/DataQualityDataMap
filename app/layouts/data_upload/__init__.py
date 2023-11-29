import streamlit as st
from .components import data


def render():
    st.markdown(body="# Upload your campaign data")
    st.divider()

    data.render()
