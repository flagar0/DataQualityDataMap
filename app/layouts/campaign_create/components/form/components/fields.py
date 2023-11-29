import streamlit as st
import datetime


def render():
    st.text_input(
        key="campaign_name_input",
        label="Campaign Name",
    )

    next_year = 2024
    jan_1 = datetime.date(2015, 1, 1)
    dec_31 = datetime.date(next_year, 12, 31)

    st.date_input(
        "Select the period of data collection",
        (jan_1, datetime.date(next_year, 1, 7)),
        jan_1,
        dec_31,
        format="MM.DD.YYYY",
        key="campaign_dates_input",
    )

    st.text_area(
        key="campaign_description_input",
        label="Campaign Description (Optional)",
    )

    # st.date_input(
    #     key="campaign_dates_input",
    #     label="Select the period of data collection",
    #     value=[None, None],
    #     format="YYYY-MM-DD",
    # )
