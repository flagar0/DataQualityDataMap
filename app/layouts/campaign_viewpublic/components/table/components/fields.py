import streamlit as st
import datetime


def timestamp_parser():
    st.text_input(
        key="timestamp_parser",
        label="Insert relevant fstring",
    )


def render():
    st.text_input(
        key="instrument_name_input",
        label="Instrument Name",
    )

    st.text_area(
        key="instrument_description_input",
        label="Instrument Description (Optional)",
    )


    # st.date_input(
    #     key="campaign_dates_input",
    #     label="Select the period of data collection",
    #     value=[None, None],
    #     format="YYYY-MM-DD",
    # )
