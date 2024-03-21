import requests
import json
import streamlit as st
import datetime
import pandas as pd
#import utils.ibge
#import components.location.state_city
#import config.init_state
#from streamlit import _RerunData, _RerunException
from streamlit.source_util import get_pages

from streamlit_extras.switch_page_button import switch_page


#streamlit run /home/flaviomidea/Documents/GitHub/DataQualityDataMap/app.py

def main():
    campaign_new_bt = st.button("Create New Campaign")
    campaign_exist_bt = st.button("Administer Existing Campaigns")
    if campaign_new_bt:
        switch_page("campanha")
    if campaign_exist_bt:
        switch_page("AdministerCampaigns")



if __name__ == "__main__":
    # demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    # page_names_to_funcs[demo_name]()    
    main()
    #main()
