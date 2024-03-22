import streamlit as st
import datetime
import pandas as pd
import config.init_state
import uuid
#from streamlit import _RerunData, _RerunException
from streamlit_extras.switch_page_button import switch_page

import database as db


def main():

    
    config.init_state.location.init()
    #st.title("Streamlit IBGE Test")
    st.title("Create a new Campaign")
    today = datetime.datetime.now()
    next_year = 2024
    jan_1 = datetime.date(2015, 1, 1)
    dec_31 = datetime.date(next_year, 12, 31)

    Campaign_name = st.text_input("Campaign Name")

    campaign_id = uuid.uuid4().hex

    d = st.date_input(
        "Select the period of data collection",
        (jan_1, datetime.date(next_year, 1, 7)),
        jan_1,
        dec_31,
        format="MM.DD.YYYY",
    )

    scientific_instruments = [ #instruments will come from campaign data in the future
        "Weather Stations",
        "Radiosondes",
        "LIDAR",
        "Ceilometers",
        "Spectrometers",
        "Ozone Monitors",
        "Aerosol Samplers",
        "Nephelometers",
        "Gas Chromatographs",
        "Pyranometers",
        "Rain Gauges",
        "Thermometers and Hygrometers",
        "Other"
    ]

    

    #selected_state, selected_city = components.location.state_city.render()
    selected_instrument = st.selectbox("Selecione um instrumento", scientific_instruments )
    if selected_instrument == "Other":
        selected_instrument = st.text_input("New Instrument")

    if st.button("Submeter"):
        st.session_state.table_data.append((Campaign_name, campaign_id, d, selected_instrument))

    # Display delete options
    delete_options = [""] + [f"{data[1]} - {data[2]}" for data in st.session_state.table_data]
    selected_delete = st.selectbox("Select the item for deletion", delete_options)

    if st.button("Delete Item"):
        if selected_delete and selected_delete != "":
            # Remove selected item from table data
            selected_index = delete_options.index(selected_delete) - 1
            if selected_index >= 0:
                st.session_state.table_data.pop(selected_index)

    if st.session_state.table_data:
        df = pd.DataFrame(st.session_state.table_data, columns=["Campaign Name", "Campaign ID", "Period Active", "Instruments used"])
        st.write("Campaigns so far:")
        st.write(df.to_html(escape=False), unsafe_allow_html=True)
        #st.dataframe(df.style, unsafe_allow_html=True)
        # st.table(df)

    submitted = st.button("Save Data")
    if submitted:
            db.insert_period(Campaign_name, campaign_id, str(d), selected_instrument)
            st.success("Data saved!")
            switch_page("AdministerCampaigns")
    
    # want_to_contribute = st.button("Create New Campaign")
    # if want_to_contribute:
    #     switch_page("NewCampaign.py")
    

    
if __name__ == "__main__":
    # demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    # page_names_to_funcs[demo_name]()    
    main()
    #main()