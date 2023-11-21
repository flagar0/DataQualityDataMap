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

    
    
def load_data(file):
     data = pd.read_csv(file)
     #data['X'] = pd.to_datetime(data['Date&TimeControl'])  # Convert the 'X' column to DateTime
     data['X'] = pd.to_datetime(data['Date&TimeControl'], unit='s')
     return data


# def switch_page(page_name: str):
#     #from streamlit import _RerunData, _RerunException
#     #from streamlit.source_util import get_pages

#     def standardize_name(name: str) -> str:
#         return name.lower().replace("_", " ")
    
#     page_name = standardize_name(page_name)

#     pages = get_pages("main")  # OR whatever your main page is called

#     print(f"Could not find page {page_name}. Must be one of {pages}")

#     #raise ValueError(f"Could not find page {page_name}. Must be one of {pages}")

#     for page_hash, config in pages.items():
#         if standardize_name(config["page_name"]) == page_name:
#             raise _RerunException(
#                 _RerunData(
#                     page_script_hash=page_hash,
#                     page_name=page_name,
#                 )
#             )

#     page_names = [standardize_name(config["page_name"]) for config in pages.values()]

#     raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")

def show_form():
    st.subheader("Input Location and Phone Numbers")

    # Input fields for location and phone numbers
    location = st.text_input("Location", "")
    phone_number = st.text_input("Phone Number", "")

    # You can add more input fields as needed

    # Submit button to process the data
    if st.button("Submit"):
        # Process the data (you can add your logic here)
        st.success(f"Location: {location}\nPhone Number: {phone_number}\nForm submitted successfully!")


def datasubmission_demo():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo ilustrates plotting capabilities
"""
    )

    want_to_contribute = st.button("I want to contribute!")
    if want_to_contribute:
        switch_page("newpage")



    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    # for i in range(1, 101):
    #     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    #     status_text.text("%i%% Complete" % i)
    #     chart.add_rows(new_rows)
    #     progress_bar.progress(i)
    #     last_rows = new_rows
    #     time.sleep(0.05)



    # file uploader for CSV
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # put CSV file into a DataFrame
        df_uploaded = pd.read_csv(uploaded_file)

        # display the uploaded data
        st.write("Uploaded Data:")
        #st.table(df_uploaded)

        # add the uploaded data to the session_state.table_data
        st.session_state.table_data.extend(df_uploaded.values.tolist())

    df = pd.read_csv(uploaded_file)
    st.line_chart(df)

    data = load_data(uploaded_file)

    st.write("Sample Data:")
    st.write(data.head())


    # st.write("Line Graph:")
    # fig, ax = plt.subplots()
    # ax.plot(data['X'], data['Y'])
    # ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # Automatically format X-axis as DateTime
    # ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))  # Customize DateTime format
    # plt.xlabel('Date and Time')
    # plt.ylabel('Y Values')
    st.pyplot()



    # st.write("Line Graph:")
    # plt.plot(data['Date&TimeControl'], data['Temp_1'])
    # plt.xlabel('Date and Time')
    # plt.ylabel('Y Values')
    # st.pyplot()

    # st.write("Graph:")
    # plt.bar(data['Date&TimeControl'], data['Temp_1'])
    # st.pyplot()


    # progress_bar = st.sidebar.progress(0)
    # status_text = st.sidebar.empty()
    # last_rows = np.random.randn(1, 1)
    # chart = st.line_chart(last_rows)

    # for i in range(1, 101):
    #     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    #     status_text.text("%i%% Complete" % i)
    #     chart.add_rows(new_rows)
    #     progress_bar.progress(i)
    #     last_rows = new_rows
    #     time.sleep(0.05)

    # progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")

page_names_to_funcs = {
    "Data Quality Report": main,
    "Data Submission Demo": datasubmission_demo,
    #"Mapping Demo": mapping_demo,
    #"DataFrame Demo": data_frame_demo
}


if __name__ == "__main__":
    demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()    
    #main()
    #main()
