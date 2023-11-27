import requests
import json
import streamlit as st
import datetime
import pandas as pd
import utils.ibge
import components.location.state_city
import config.init_state

# from streamlit import _RerunData, _RerunException
from streamlit.source_util import get_pages

from streamlit_extras.switch_page_button import switch_page

import calendar  # Core Python Module
import plotly.graph_objects as go  # pip install plotly
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu

import database as db  # local import


def main():
    st.header("Data Visualization")
    with st.form("saved_periods"):
        period = st.selectbox("Select Period:", get_all_periods())
        submitted = st.form_submit_button("Plot Period")


if __name__ == "__main__":
    # demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    # page_names_to_funcs[demo_name]()
    main()
    # main()
