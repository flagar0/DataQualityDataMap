import streamlit as st
from .components import fields
from .components import validate
from .components import submit
from time import sleep


def render():
    with st.form(key="form_campaign_create"):
        fields.render()
        if st.form_submit_button(label="Login"):
            flag = validate.exec()
            if flag:
                submit.exec()
                with st.spinner(text="Please wait..."):
                    sleep(2)
                    st.rerun()
