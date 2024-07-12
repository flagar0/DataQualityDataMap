import streamlit as st
import pandas as pd
import pymongo

import config.db.mongo
from schemas import Campaign
import json

import streamlit_antd_components as sac

import bunnet as bn
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_timeline import st_timeline

# from typing import Optional
# from bunnet import Document


from time import sleep

from streamlit_extras import stateful_button as stb

user_id = "a"
sns.set_theme(style="whitegrid") #tema

def get_campaigns_by_user(user):
    client = st.session_state.mongo_client

    bn.init_bunnet(database=client.newbase, document_models=[Campaign])
    result = Campaign.find_all().to_list()
    return result

def get_plot():
    return

def mongoexport(df, db_name, coll_name): # USANDO PYMONGO
    """Export a panda file from a mongo colection
    returns: panda data
    """
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db[coll_name]
    return pd.DataFrame(list(coll.find(projection={'_id': False}))) ## tirar o _id e limita para nao travar

def delete_campaign(delete):
    client = st.session_state.mongo_client

    bn.init_bunnet(database=client.newbase, document_models=[Campaign])

    Campaign.find_one(Campaign.name == delete).delete()

def get_camaign_names(df,x_axis,y_axis):

    return sns.lineplot(data=df, x=x_axis, y=y_axis, markers=True)


def get_campaign_dq(db_name, id): # db_name: newbase
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db["Dataquality"]
    return pd.DataFrame(list(coll.find({"collection_id": id},projection={'_id': False}, limit=0)))  ## tirar o _id e limita para nao travar
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
            ],
        )
        if selected_campaign:
            df = mongoexport(df,
                             "newbase",
                             # "newcollection",
                             selected_campaign.collection_id, )
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
                    ],
                )

                if(plots == "Scatter Plot"):
                    x_axis = st.selectbox("Select X-axis", options=df.columns, index=0,
                                          disabled=False)
                    y_axis = st.selectbox("Select Y-axis", options=df.columns, index=1)
                    st.subheader("Scatter Plot")
                    fig = plt.figure(figsize=(10, 5))
                    sns.scatterplot(data=df, x=x_axis, y=y_axis)
                    st.pyplot(fig)
                    st.session_state.x_disabled = False

                elif(plots == "Box Plot"):
                    x_axis = st.selectbox("Select X-axis", options=df.columns, index=0,
                                          disabled=True)
                    y_axis = st.selectbox("Select Y-axis", options=df.columns, index=1)
                    st.subheader("Box Plot")
                    fig2 = plt.figure(figsize=(10, 5))
                    sns.boxplot(data=df, x=y_axis)
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
                dq = get_campaign_dq("newbase", selected_campaign.collection_id)
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
                #st.subheader("Selected item")
                #st.write(timeline)
                #fim data timeline