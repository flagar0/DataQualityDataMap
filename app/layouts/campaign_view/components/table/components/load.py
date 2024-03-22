import streamlit as st
import pandas as pd
import pymongo

import config.db.mongo
from schemas import Campaign
import json

import streamlit_antd_components as sac

import bunnet as bn


# from typing import Optional
# from bunnet import Document


from time import sleep

from streamlit_extras import stateful_button as stb

user_id = "a"


def get_campaigns_by_user(user):
    client = st.session_state.mongo_client

    bn.init_bunnet(database=client.newbase, document_models=[Campaign])
    result = Campaign.find_all().to_list()

    return result


# def create_new_campaigncollection(campaign_id):
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = myclient["newbase"]

#     mycol = mydb[campaign_id]

#     return


# def mongoimport(csv_path, db_name, coll_name, db_url='localhost', db_port=27000):
# def mongoimport(csv_path, db_name, coll_name):
def mongoimport(df, db_name, coll_name):
    """Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db[coll_name]
    # data = pd.read_csv(csv_path)
    payload = df.to_dict(orient="records")

    # coll.delete_many()
    coll.insert_many(payload)
    return coll.estimated_document_count()


def delete_campaign(delete):
    client = st.session_state.mongo_client

    bn.init_bunnet(database=client.newbase, document_models=[Campaign])

    Campaign.find_one(Campaign.name == delete).delete()


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

        opts = [""] + user_campaigns_list
        selected_campaign = st.selectbox(
            label="Select a campaign to manage",
            options=opts,
            index=0,
        )



