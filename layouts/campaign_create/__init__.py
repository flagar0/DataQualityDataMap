import streamlit as st
from .components import form


def render():
    st.markdown(body="# Create a new campaign")
    st.divider()

    form.render()

    # await asyncio.run(form.render())
