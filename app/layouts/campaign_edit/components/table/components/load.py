import streamlit as st
import pandas as pd
import datetime
import config.db.mongo
from schemas import Campaign,Dataquality,Headers
from streamlit_timeline import st_timeline
import streamlit_antd_components as sac
import bunnet as bn
import numpy as np
# from typing import Optional
# from bunnet import Document


from time import sleep

from streamlit_extras import stateful_button as stb

user_id = "a"

colors = {
        'yellow': '#FFFF00',
        'white': '#F3F3F3',
        'black': '#000000'
    }

next_year = 2024
jan_1 = datetime.date(2012, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

def get_campaigns_by_user(user):
    client = st.session_state.mongo_client
    user = st.session_state.auth.user
    bn.init_bunnet(database=client.info, document_models=[Campaign])
    result = Campaign.find({"user_id":user}).to_list()

    return result

def delete_campaign(delete,collection_id):
    client = st.session_state.mongo_client
    user = st.session_state.auth.user
    db = client[user]
    db.drop_collection(collection_id)

    bn.init_bunnet(database=client[user], document_models=[Headers.Headers])
    Headers.Headers.find(Headers.Headers.name == delete).delete().run()

    bn.init_bunnet(database=client[user], document_models=[Dataquality])
    Dataquality.find(Dataquality.name == delete).delete().run()

    bn.init_bunnet(database=client.info, document_models=[Campaign])
    Campaign.find_one(Campaign.name == delete).delete().run()

def get_header(db_name, id):
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db["Headers"]
    return pd.DataFrame(coll.find({"collection_id": id},projection={'_id': False}, limit=0))['header'][0]  ## tirar o _id e limita para nao travar

def upload_header(header,selected_campaign):
    client = st.session_state.mongo_client
    user = st.session_state.auth.user
    bn.init_bunnet(database=client[user], document_models=[Headers.Headers])
    dq = Headers.Headers(
            name=selected_campaign.name,
            user_id=selected_campaign.user_id,
            collection_id=selected_campaign.collection_id,
            header=header
        )
    dq.insert()
    return True #BaseException as e

def get_campaign_dq(db_name, id): # data quality
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db["Dataquality"]
    return pd.DataFrame(list(coll.find({"collection_id": id},projection={'_id': False}, limit=0)))  ## tirar o _id e limita para nao travar

def update_dataquality(data_quality,selected_campaign):
    try:
        client = st.session_state.mongo_client
        user = st.session_state.auth.user
        db = client[user]
        coll = db["Dataquality"]
        coll.update_one({"collection_id": selected_campaign}, {"$set": {"data": data_quality}})
        return True #BaseException as e
    except BaseException as e:
        print(e)
        return False

def render():
    st.session_state.table_data = st.session_state.get("table_data", [])
    if 'data_quality' not in st.session_state:  st.session_state.data_quality = []



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
                    sac.SegmentedItem(label="Data Quality"),
                    sac.SegmentedItem(label="Delete")
                ], )

            if (escolha=="Edit Header"):
                header_list = get_header(
                             user,
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

            if (escolha=="Data Quality"):
                st.markdown(
                    '<div style="display: block ruby;"> <div style="background-color: #FFFF00; width: 15px; height: 15px; padding-right:2px;"></div> Suspect </div>'
                    '<div style="display: block ruby;"> <div style="background-color: #F3F3F3; width: 15px; height: 15px; padding-right:2px;"></div> Note </div>'
                    '<div style="display: block ruby;"> <div style="background-color: black; width: 15px; height: 15px; padding-right:2px;"></div> Incorrect </div>',
                    unsafe_allow_html=True
                )
                selected_color = st.selectbox("Select a quality level", list(colors.keys()))
                # Data Quality

                if st.session_state.data_quality == []:
                    st.session_state.data_quality = get_campaign_dq(user,selected_campaign.collection_id)["data"][0]
                data_quality = st.session_state.data_quality

                if selected_color:
                    st.markdown(
                        f'<div style="background-color: {colors[selected_color]}; width: 50px; height: 50px;"></div>',
                        unsafe_allow_html=True
                    )
                st.write(f'Selected quality: {selected_color}')

                if (selected_color == "white"):
                    note_disabled = False
                else:
                    note_disabled = True
                note = st.text_area(label="Note", disabled=note_disabled)
                date = st.date_input(
                    "Select the period of data collection",
                    (jan_1, datetime.date(next_year, 1, 7)),
                    jan_1,
                    dec_31,
                    format="MM.DD.YYYY",  # 2014-09-01 00:12:32
                )
                hour_min = st.time_input("Start time", step=60)
                hour_max = st.time_input("End time", step=60)

                start_datetime = datetime.datetime.combine(date[0], hour_min)
                end_datetime = datetime.datetime.combine(date[1], hour_max)

                st.divider()  # ------------------
                st.subheader("Preview Timeline")

                if (data_quality != None):
                    analise = st.selectbox("Select Data", options=list(data_quality))
                    items = []
                    for g in data_quality[analise]["green"]:  # verdes
                        items.append(g)
                    for r in data_quality[analise]["red"]:
                        items.append(r)
                    for y in data_quality[analise]["yellow"]:
                        items.append(y)
                    for w in data_quality[analise]["white"]:
                        items.append(w)
                    for b in data_quality[analise]["black"]:
                        items.append(b)

                    items_new = items
                    col_prev, col_add = st.columns(2)
                    bool_add_btn = True
                    with col_prev:
                        if (st.button("Preview")):  # "style": "background-color: selected color;"
                            items_new.append({"start": str(start_datetime), "end": str(end_datetime),
                                              "style": "background-color: " + colors[selected_color] + ";"})
                            bool_add_btn = False
                    with col_add:
                        if (st.button("Add", disabled=bool_add_btn)):
                            data_quality[analise][selected_color].append(
                                {"start": str(start_datetime), "end": str(end_datetime),
                                 "style": "background-color: " + colors[selected_color] + ";"})
                            items_new.append({"start": str(start_datetime), "end": str(end_datetime),
                                              "style": "background-color: " + colors[selected_color] + ";"})
                            if (note != ""):
                                data_quality[analise]["note"] = note
                            st.session_state.data_quality = data_quality
                    if (st.button("Clear")):
                        bool_add_btn = True

                    timeline = st_timeline(items_new, groups=[], options={
                        "snap": None,
                        "stack": False,
                        "selectable": False,
                    })
                    if (note != ""):
                        st.markdown(
                            f'<div style="diplay: -webkit-box;"> <div style="background-color: #FFFF; width: 15px; height: 15px; padding-right:2px;"></div> Note: {note}</div>',
                            unsafe_allow_html=True
                        )

                    if stb.button("Upload Data Quality",key="up_dq"):
                        if update_dataquality(st.session_state.data_quality, selected_campaign.collection_id):
                            st.success(
                                f"Data Quality Added Successfully to Campaign {selected_campaign.name}"
                            )
                            st.session_state.data_quality = []


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
                                    delete_campaign(selected_campaign.name,selected_campaign.collection_id)
                                    st.success("Deleted!")

                                    st.session_state.table_data = None
                                    st.session_state.btn_delete = False

                                    with st.spinner("Please wait..."):
                                        sleep(2)
                                        st.rerun()
