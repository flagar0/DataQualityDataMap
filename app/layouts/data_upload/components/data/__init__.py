import streamlit as st
from .components import upload


def render():
    upload.render()
    # with st.form(key="form_campaign_create"):
    #     load.render()
