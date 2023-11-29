import streamlit as st
import pandas as pd

import config.db.mongo
from schemas import Campaign

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
            label="Select the item for deletion",
            options=opts,
            index=0,
        )

        if selected_campaign:
            if stb.button("Delete Item", key="btn_delete"):
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
                            selected_index = opts.index(selected_campaign) - 1
                            if selected_index >= 0:
                                delete_campaign(selected_campaign.name)
                                st.success("Deleted!")

                                st.session_state.table_data = None
                                st.session_state.btn_delete = False

                                with st.spinner("Please wait..."):
                                    sleep(2)
                                    st.rerun()
