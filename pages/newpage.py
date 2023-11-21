import requests
import json
import streamlit as st
import datetime
import pandas as pd
import utils.ibge
import components.location.state_city
import config.init_state
#from streamlit import _RerunData, _RerunException
from streamlit.source_util import get_pages

from streamlit_extras.switch_page_button import switch_page




def main():

    
    config.init_state.location.init()
    #st.title("Streamlit IBGE Test")
    st.title("Data Insertion Test")
    today = datetime.datetime.now()
    next_year = 2024
    jan_1 = datetime.date(2015, 1, 1)
    dec_31 = datetime.date(next_year, 12, 31)



    d = st.date_input(
        "Select the period of data collection",
        (jan_1, datetime.date(next_year, 1, 7)),
        jan_1,
        dec_31,
        format="MM.DD.YYYY",
    )

    colors = {
        'Vermelho': '#FF0000',
        'Verde': '#00FF00',
        'Amarelo': '#FFFF00',
        'Branco': '#FFFFFF',
        'Preto': '#000000'
    }

    selected_color = st.selectbox("Selecione um nível de qualidade", list(colors.keys()))

    if selected_color:
        st.markdown(
            f'<div style="background-color: {colors[selected_color]}; width: 50px; height: 50px;"></div>',
            unsafe_allow_html=True
        )
    st.write(f'Qualidade Selecionada: {selected_color}')

    selected_value = pd.DataFrame({'': [f'<div style="background-color: {colors[selected_color]}; width: 50px; height: 50px;"></div>']})

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
        "Thermometers and Hygrometers"
    ]

    

    #selected_state, selected_city = components.location.state_city.render()
    selected_instrument = st.selectbox("Selecione um instrumento", scientific_instruments )

    selected_Campaign = st.text_input("Campaign")
    selected_extra = st.text_input("Projeto")

        # Create a button to open the form
    if st.button("Open Form3"):
        # Create a modal popup for the form
        with st.form("my_form"):
            st.subheader("Input Location and Phone Numbers")

            # Input fields for location and phone numbers
            location = st.text_input("Location")
            phone_number = st.text_input("Phone Number")

            # Submit button to process the data
            submit_button = st.form_submit_button("Submit")

        # Process the form data when the submit button is clicked
        if submit_button:
            # Process the data (you can add your logic here)
            st.success(f"Location: {location}\nPhone Number: {phone_number}\nForm submitted successfully!")

    if st.button("Open Form2"):
        st.markdown(
            """
            <style>
                .popup-btn {
                    display: inline-block;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    text-align: center;
                    text-decoration: none;
                    outline: none;
                    color: #fff;
                    background-color: #4CAF50;
                    border: none;
                    border-radius: 15px;
                    box-shadow: 0 9px #999;
                }

                .popup-content {
                    display: none;
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background-color: #fefefe;
                    padding: 20px;
                    border: 1px solid #888;
                    width: 300px;
                    border-radius: 10px;
                    z-index: 1;
                }

                .close {
                    color: #aaa;
                    float: right;
                    font-size: 28px;
                    font-weight: bold;
                }

                .close:hover,
                .close:focus {
                    color: black;
                    text-decoration: none;
                    cursor: pointer;
                }
            </style>
            """
            , unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="popup-btn" onclick="openForm()">Open Form</div>
            <div class="popup-content" id="form">
                <span class="close" onclick="closeForm()">&times;</span>
                <h2>Location and Phone Number Form</h2>
                <form>
                    <label for="location">Location:</label>
                    <input type="text" id="location" name="location">

                    <label for="phone_number">Phone Number:</label>
                    <input type="text" id="phone_number" name="phone_number">

                    <button type="button" onclick="submitForm()">Submit</button>
                </form>
            </div>
            <script>
                function openForm() {
                    document.getElementById('form').style.display = 'block';
                }

                function closeForm() {
                    document.getElementById('form').style.display = 'none';
                }

                function submitForm() {
                    // You can add your logic to process the form data here
                    alert('Form submitted successfully!');
                    closeForm();
                }
            </script>
            """
            , unsafe_allow_html=True
        )

    
    if st.button("Open Form"):
        show_form()

    #switch_page("app")


    if st.button("Submeter"):
        st.session_state.table_data.append((d, selected_instrument, selected_Campaign, selected_extra, selected_value))

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
        df = pd.DataFrame(st.session_state.table_data, columns=["Date", "Instrument", "Campaign", "Project", "Data Quality"])
        st.write("Data So Far:")
        st.write(df.to_html(escape=False), unsafe_allow_html=True)
        #st.dataframe(df.style, unsafe_allow_html=True)
        # st.table(df)
    
    want_to_contribute = st.button("Create New Campaign")
    if want_to_contribute:
        switch_page("NewCampaign")
    

    
if __name__ == "__main__":
    # demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    # page_names_to_funcs[demo_name]()    
    main()
    #main()