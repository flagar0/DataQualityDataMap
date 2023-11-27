import streamlit as st
from .components import load
import asyncio


def render():
    load.render()
    # with st.form(key="form_campaign_create"):
    #     load.render()
