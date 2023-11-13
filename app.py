import requests
import json
import streamlit as st
import datetime
import pandas as pd
import utils.ibge
import components.location.state_city
import config.init_state


def main():

    
    config.init_state.location.init()
    #st.title("Streamlit IBGE Test")
    st.title("Data Insertion Test")
    today = datetime.datetime.now()
    next_year = 2015
    jan_1 = datetime.date(next_year, 1, 1)
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
        'Amarelo': '#FFFF00'
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


def datasubmission_demo():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!
"""
    )

    # file uploader for CSV
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # put CSV file into a DataFrame
        df_uploaded = pd.read_csv(uploaded_file)

        # display the uploaded data
        st.write("Uploaded Data:")
        st.table(df_uploaded)

        # add the uploaded data to the session_state.table_data
        st.session_state.table_data.extend(df_uploaded.values.tolist())

    data = load_data(uploaded_file)

    st.write("Sample Data:")
    st.write(data.head())


    st.write("Line Graph:")
    fig, ax = plt.subplots()
    ax.plot(data['X'], data['Y'])
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # Automatically format X-axis as DateTime
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))  # Customize DateTime format
    plt.xlabel('Date and Time')
    plt.ylabel('Y Values')
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
