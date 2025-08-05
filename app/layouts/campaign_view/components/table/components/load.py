import streamlit as st
import pandas as pd
import pymongo
import xarray
import config.db.mongo
from schemas import Campaign
import json

import streamlit_antd_components as sac

import bunnet as bn
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_timeline import st_timeline
from config.functions import *
# from typing import Optional
from pygwalker.api.streamlit import StreamlitRenderer
# from bunnet import Document


from time import sleep

from streamlit_extras import stateful_button as stb

user_id = "a"
sns.set_theme(style="whitegrid") #tema

@st.cache_resource
def get_pyg_renderer(dados) -> "StreamlitRenderer":
    df = dados
    # If you want to use feature of saving chart config, set `spec_io_mode="rw"`
    return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw")
def render():
    st.session_state.table_data = st.session_state.get("table_data", [])

    # TO-DO inicializar table_data com None
    # TO-DO trocar nome table_data para campaing list

    user = st.session_state.auth.user
    user_campaigns_list = get_campaigns_by_user(user)

    st.session_state.table_data = []
    for campaign in user_campaigns_list:
        Campaign_name = campaign.name
        description = campaign.description
        date = campaign.date

        st.session_state.table_data.append((Campaign_name, description, date))

    if st.session_state.table_data:
        df = pd.DataFrame(
            st.session_state.table_data,
            columns=["name", "description", "date"],
        )
        st.dataframe(
            data=df,
            hide_index=True,
            column_order=["name", "description", "date"],
            column_config={
                "name": st.column_config.TextColumn(label="Name"),
                "description": st.column_config.TextColumn(label="Description"),
                "date": st.column_config.TextColumn(label="Date"),
            },
        )

        selected_campaign = st.selectbox(
            label="Select a campaign to manage",
            options=user_campaigns_list,
            index=None,
            format_func=lambda x: x.name,
        )

        escolha = sac.segmented(
            items=[
                sac.SegmentedItem(label="Data View"),
                sac.SegmentedItem(label="Data Timeline"),
                sac.SegmentedItem(label="Download"),
            ],
        )
        if selected_campaign:
            df = mongoexport(df,
                             user,
                             # "newcollection",
                             selected_campaign.collection_id, )
            try:
                df["time"] = pd.to_datetime(df["time"])
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                df["time_offset"] = pd.to_datetime(df["time_offset"])
            except:
                print("Sem coluna de tempo")

            if (escolha == "Data View"):
            #Aba view data


                st.subheader("Data View")
                num_rows = st.number_input(
                    "Number of Rows to Display", min_value=1, max_value=10000, value=10
                )
                st.write(f"Displaying the top {num_rows} rows of the DataFrame:")
                st.write(df.head(num_rows))

                st.subheader("Missing Values")
                st.write("Number of missing values in each column:")
                st.write(df.isnull().sum())

                st.subheader("Summary Statistics")
                st.write(df.describe())


                # plots

                plots = sac.segmented(
                    items=[
                        sac.SegmentedItem(label="Scatter Plot"),
                        sac.SegmentedItem(label="Box Plot"),
                        sac.SegmentedItem(label="Histogram"),
                        sac.SegmentedItem(label="Interactive")
                    ],
                )

                if(plots == "Scatter Plot"):
                    x_axis = st.selectbox("Select X-axis", options=df.columns, index=0,
                                          disabled=False)
                    y_axis = st.selectbox("Select Y-axis", options=df.columns, index=1)
                    st.subheader("Scatter Plot")
                    fig = plt.figure(figsize=(10, 5))
                    start_x, end_x = st.select_slider("Select a range for X-axis:",options=df[x_axis],value=(df[x_axis][0],df[x_axis][len(df[x_axis])-1]))
                    df_mod = df
                    df_list = list(df[x_axis])
                    df_mod[x_axis] = df_mod[x_axis][df_list.index(start_x) : df_list.index(end_x)]
                    ax = sns.scatterplot(data=df_mod, x=x_axis, y=y_axis,s=10)
                    ax.tick_params(axis='x', labelrotation=45)
                    st.pyplot(fig)
                    st.session_state.x_disabled = False

                elif(plots == "Box Plot"):
                    x_axis = st.selectbox("Select X-axis", options=df.columns, index=0,
                                          disabled=True)
                    y_axis = st.selectbox("Select Y-axis", options=df.columns, index=1)
                    st.subheader("Box Plot")
                    fig2 = plt.figure(figsize=(10, 5))
                    print(df.columns)
                    sns.boxplot(x=df['n7'])
                    st.pyplot(fig2)
                    st.session_state.x_disabled = True

                elif (plots == "Histogram"):
                    x_axis = st.selectbox("Select X-axis", options=df.columns, index=0,
                                          disabled=True)
                    y_axis = st.selectbox("Select Y-axis", options=df.columns, index=1)
                    print(st.session_state.x_disabled)
                    st.subheader("Histogram")
                    fig3 = plt.figure(figsize=(10, 5))
                    sns.histplot(data=df, x=y_axis)
                    st.pyplot(fig3)
                    st.session_state.x_disabled = True
                elif (plots == "Interactive"):
                    renderer = get_pyg_renderer(df)
                    renderer.explorer()


            #Fim data view

            elif(escolha == "Data Timeline"):
                #Data timeline
                st.subheader("Timeline")
                st.markdown(
                    '<div style="display: block ruby;"> <div style="background-color: green; width: 15px; height: 15px; padding-right:2px;"></div> Ok </div>'
                    '<div style="display: block ruby;"> <div style="background-color: red; width: 15px; height: 15px; padding-right:2px;"></div> Missing </div>'
                    '<div style="display: block ruby;"> <div style="background-color: #FFFF00; width: 15px; height: 15px; padding-right:2px;"></div> Suspect </div>'
                    '<div style="display: block ruby;"> <div style="background-color: #F3F3F3; width: 15px; height: 15px; padding-right:2px;"></div> Note </div>'
                    '<div style="display: block ruby;"> <div style="background-color: black; width: 15px; height: 15px; padding-right:2px;"></div> Incorrect </div>',
                    unsafe_allow_html=True
                )
                dq = get_campaign_dq(user, selected_campaign.collection_id)
                dq = dq["data"][0]

                analise = st.selectbox("Select Data", options=list(dq))
                items=[]
                for g in dq[analise]["green"]: #verdes
                    items.append((g))
                for r in dq[analise]["red"]:
                    items.append((r))
                for y in dq[analise]["yellow"]:
                    items.append(y)
                for w in dq[analise]["white"]:
                    items.append(w)
                for b in dq[analise]["black"]:
                    items.append(b)

                timeline = st_timeline(items, groups=[], options={
                    "snap": None,
                    "stack": False,
                    "selectable": False,
                })
                if (dq[analise]["note"] != None):
                    st.markdown(
                        f'<div style="display: block ruby;"> <div style="background-color: #F3F3F3; width: 15px; height: 15px; padding-right:2px;"></div> Note: {dq[analise]["note"]}</div>',
                        unsafe_allow_html=True
                    )


            elif (escolha == "Download"):
                df_header = get_header(user, selected_campaign.collection_id)

                df = df.set_index("time")
                ds = xarray.Dataset(df)
                separado = ds.groupby("time.date")
                div_data = list(separado.groups.keys())

                formato = st.radio(
                    "Choose a format to download:",
                    [".csv", ".cdf", ".nc"],
                    key="formato",
                    horizontal=True
                )
                col1, col2 = st.columns(2)
                with col1:
                    with st.popover("Time Range"):
                        start_dia, end_dia = st.select_slider(
                            "Select a range of download",
                            options=div_data,
                            value=(div_data[0],div_data[-1]),
                        )
                with col2:
                    with st.spinner("Processing..."):
                        zip = download_campaign(ds,df_header,formato,(start_dia, end_dia),user,selected_campaign.name)
                    st.download_button(
                        label="📥Download",
                        data=zip,
                        file_name=f"{user}_{selected_campaign.name}.zip",
                        mime="application/zip",
                    )



