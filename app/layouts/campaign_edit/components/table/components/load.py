import streamlit as st
import pandas as pd

import config.db.mongo
from schemas import Campaign

import streamlit_antd_components as sac
import bunnet as bn
from schemas import Headers
import numpy as np
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

def delete_campaign(delete):
    client = st.session_state.mongo_client

    bn.init_bunnet(database=client.newbase, document_models=[Campaign])

    Campaign.find_one(Campaign.name == delete).delete()

def get_header(db_name, id):
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db["Headers"]
    return pd.DataFrame(coll.find({"collection_id": id},projection={'_id': False}, limit=0))['header'][0]  ## tirar o _id e limita para nao travar

def upload_header(header,selected_campaign):
    client = st.session_state.mongo_client
    bn.init_bunnet(database=client.newbase, document_models=[Headers.Headers])
    user = st.session_state.auth.user
    dq = Headers.Headers(
            name=selected_campaign.name,
            user_id=selected_campaign.user_id,
            collection_id=selected_campaign.collection_id,
            header=header
        )
    dq.insert()
    return True #BaseException as e
def render():
    st.session_state.table_data = st.session_state.get("table_data", [])

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
            label="Select the item for edit",
            options=user_campaigns_list,
            index=None,
            format_func=lambda x: x.name
        )

        if selected_campaign:
            escolha = sac.segmented(
                items=[
                    sac.SegmentedItem(label="Edit Header"),
                    sac.SegmentedItem(label="Delete"),
                ], )

            if (escolha=="Edit Header"):
                header_list = get_header(
                             "newbase",
                             # "newcollection",
                             selected_campaign.collection_id)

                cdf_header = [""] * len(list(header_list))#

                for i in range(len(cdf_header)):
                    cdf_header[i] = header_list[list(header_list)[i]]

                df_header = pd.DataFrame(data={"Data Header":list(header_list),"Data Description":cdf_header})
                header_description = st.data_editor(df_header ,use_container_width=True,hide_index=True,disabled=["Data Header"])

                if stb.button("Update Header",key="btn_header"):
                    if upload_header(dict(header_description), selected_campaign):
                        st.success(
                            f"Header Description Updated Successfully to Campaign {selected_campaign.name}"
                        )

            if(escolha =="Delete"):
                btn_pass = True
                db_name = st.text_input("Type '"+selected_campaign.name+"' to confirm your action")
                if db_name == selected_campaign.name:
                    btn_pass = False
                else:
                    st.session_state.btn_delete = False
                    btn_pass = True

                if stb.button("Delete Item", key="btn_delete",disabled = btn_pass):
                    st.write(
                        "Are you sure? All Data associated with this campaign will be deleted"
                    )
                    col_confirm, col_cancel = st.columns(2)
                    with col_cancel:
                        if st.button("❌ Cancel"):
                            st.session_state.btn_delete = False
                            st.rerun()

                    with col_confirm:
                        if st.button("✅ Confirm"):
                            if selected_campaign and selected_campaign != "":
                                # Remove selected item from table data
                                selected_index = user_campaigns_list.index(selected_campaign) - 1
                                if selected_index >= 0:
                                    delete_campaign(selected_campaign.name)
                                    st.success("Deleted!")

                                    st.session_state.table_data = None
                                    st.session_state.btn_delete = False

                                    with st.spinner("Please wait..."):
                                        sleep(2)
                                        st.rerun()
