import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from time import sleep

from streamlit_extras import stateful_button as stb

user_id = "a"

# st.session_state["table_data"] = ""


def render():
    st.title("CSV File Uploader and Parser")

    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        st.info("File uploaded successfully!")

        df = pd.read_csv(uploaded_file)

        st.subheader("Data Preview")
        st.dataframe(df)

        num_rows = st.number_input(
            "Number of Rows to Display", min_value=1, max_value=len(df), value=10
        )
        st.write(f"Displaying the top {num_rows} rows of the DataFrame:")
        st.write(df.head(num_rows))

        st.subheader("Missing Values")
        st.write("Number of missing values in each column:")
        st.write(df.isnull().sum())

        st.subheader("Summary Statistics")
        st.write(df.describe())

        # plot
        st.subheader("Scatter Plot")
        x_axis = df.columns[0]
        # st.selectbox("Select X-axis", options=df.columns)
        y_axis = st.selectbox("Select Y-axis", options=df.columns)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=x_axis, y=y_axis)
        st.pyplot(plt)
