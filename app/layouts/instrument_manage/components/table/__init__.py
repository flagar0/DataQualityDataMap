import streamlit as st
from .components import load


def render():
    load.render()
    # with st.form(key="form_campaign_create"):
    #     load.render()
