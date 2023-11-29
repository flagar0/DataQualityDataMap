import streamlit as st
from .components import fields
from .components import validate
from .components import submit


def render():
    with st.form(key="form_campaign_create"):
        fields.render()

        if st.form_submit_button(label="Submit"):
            # submit.exec()
            flag = validate.exec()
            if flag:
                submit.exec()
