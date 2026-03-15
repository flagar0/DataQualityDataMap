import streamlit as st
import pandas as pd
import datetime
from streamlit_timeline import st_timeline
import streamlit_antd_components as sac
# from typing import Optional
# from bunnet import Document
from config.functions import *

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

def render():
    st.session_state.table_data = st.session_state.get("table_data", [])
    if 'data_quality' not in st.session_state:  st.session_state.data_quality = []




    user_campaigns_list = get_all_campaigns()
    st.session_state.table_data = []
    for campaign in user_campaigns_list:
        Campaign_name = campaign.name
        description = campaign.description
        date = campaign.date
        public = "✅" if campaign.public == "True" else "❌"
        validated = "✅" if campaign.validated == "True" else "❌"
        usuario = campaign.user_id
        st.session_state.table_data.append((Campaign_name, description, date, public, validated, usuario))

    if st.session_state.table_data:
        df = pd.DataFrame(
            st.session_state.table_data,
            columns=["name", "description", "date", "public", "validated","user_id"],
        )
        st.dataframe(
            data=df,
            hide_index=True,
            column_order=["name", "description", "date", "public", "validated","user_id"],
            column_config={
                "name": st.column_config.TextColumn(label="Name"),
                "description": st.column_config.TextColumn(label="Description"),
                "date": st.column_config.TextColumn(label="Date"),
                "public": st.column_config.TextColumn(label="Public"),
                "validated": st.column_config.TextColumn(label="Validated"),
                "user_id": st.column_config.TextColumn(label="User ID"),
            },
        )

        selected_campaign = st.selectbox(
            label="Select the item for edit",
            options=user_campaigns_list,
            index=None,
            format_func=lambda x: f"{x.name} - {x.user_id}"
        )


        if selected_campaign:
            user = selected_campaign.user_id
            escolha = sac.segmented(
                items=[
                    sac.SegmentedItem(label="Edit Header"),
                    sac.SegmentedItem(label="Edit Info"),
                    sac.SegmentedItem(label="Data Quality"),
                    sac.SegmentedItem(label="Delete"),
                    sac.SegmentedItem(label="Export")
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

            if(escolha == "Edit Info"):
                with st.form(key="edit_campaign_form"):
                    st.write("### 📝 Campaign Information")

                    # Nome da campanha
                    new_name = st.text_input(
                        "Campaign Name",
                        value=selected_campaign.name
                    )

                    # Descrição
                    new_description = st.text_area(
                        "Description",
                        value=selected_campaign.description,
                        height=100
                    )

                    # Data
                    new_date = st.text_input(
                        "Date",
                        value=selected_campaign.date
                    )

                    st.divider()
                    st.write("### 🔒 Visibility and Validation Settings")

                    col1, col2 = st.columns(2)

                    with col1:
                        # Público
                        current_public = selected_campaign.public == "True"
                        new_public = st.checkbox(
                            "Public Campaign",
                            value=current_public,
                            help="Determines whether the campaign will be publicly visible."
                        )

                    with col2:
                        # Validada
                        current_validated = selected_campaign.validated == "True"
                        new_validated = st.checkbox(
                            "Validated Campaign",
                            value=current_validated,
                            help="Determines whether the campaign has been approved by the curator."
                        )

                    st.divider()

                    # Mostrar resumo das alterações
                    st.write("### 📋 Summary of Changes")

                    changes = []
                    if new_name != selected_campaign.name:
                        changes.append(f"• **Name:** '{selected_campaign.name}' → '{new_name}'")
                    if new_description != selected_campaign.description:
                        changes.append(f"• **Description:** Modified")
                    if new_date != selected_campaign.date:
                        changes.append(f"• **Date:** '{selected_campaign.date}' → '{new_date}'")
                    if new_public != current_public:
                        status_public = "✅ Public" if new_public else "❌ Private"
                        changes.append(f"• **Visibility:** {status_public}")
                    if new_validated != current_validated:
                        status_validated = "✅ Validated" if new_validated else "❌ Not Validated"
                        changes.append(f"• **Validation:** {status_validated}")

                    if changes:
                        st.warning("**Changes detected:**")
                        for change in changes:
                            st.write(change)
                    else:
                        st.info("ℹ️ No changes detected")

                    st.divider()

                    # Botões de ação
                    col_submit, col_reset = st.columns([1, 1])

                    with col_submit:
                        submit_button = st.form_submit_button(
                            label="💾 Save Changes",
                            type="primary",
                            use_container_width=True
                        )

                    with col_reset:
                        cancel_button = st.form_submit_button(
                            label="🔄 Reset",
                            use_container_width=True
                        )

                    if submit_button:
                        if changes:
                            # Preparar dados para atualização
                            updated_data = {
                                'name': new_name,
                                'description': new_description,
                                'date': new_date,
                                'public': "True" if new_public else "False",
                                'validated': "True" if new_validated else "False"
                            }

                            # Atualizar no banco
                            with st.spinner("Saving changes..."):
                                if update_campaign_info(selected_campaign.id, updated_data):
                                    st.success("✅ Campaign updated successfully!")
                                    # Limpar cache e recarregar
                                    with st.spinner("Refreshing list..."):
                                        sleep(1.5)
                                        st.rerun()
                                else:
                                    st.error("❌ Error updating campaign. Check logs.")
                        else:
                            st.info("ℹ️ No changes to save.")

                        if cancel_button:
                            st.info("🔄 Form reset")
                            st.rerun()

                    # Informações adicionais (somente leitura)
                    st.divider()
                    with st.expander("ℹ️ Technical Information (read-only)"):
                        st.write(f"**User ID:** `{selected_campaign.user_id}`")
                        st.write(f"**Collection ID:** `{selected_campaign.collection_id}`")
                        st.write(f"**Campaign ID:** `{selected_campaign.id}`")

            if(escolha =="Export"):
                st.subheader("📊 Export to Jupyter Notebook")
                st.write(f"**Selected Campaign:** {selected_campaign.name}")
                st.write(f"**Owner:** {user}")

                st.info("🔬 This feature exports campaign data as a .parquet file and generates ready-to-use code for Jupyter Notebook analysis.")

                if st.button("🚀 Generate Export", type="primary"):
                    with st.spinner("Exporting data to .parquet..."):
                        filepath, filename = export_campaign_to_parquet(user, selected_campaign)

                        if filepath and filename:
                            st.success("✅ Data exported successfully!")

                            # URL base do servidor
                            base_url = "http://localhost:8501"
                            jupyter_code = generate_jupyter_code(base_url, filename, selected_campaign.name)

                            st.divider()
                            st.subheader("📝 Generated Jupyter Notebook")
                            st.write("Download the .ipynb file to use in Jupyter Notebook or Google Colab:")

                            st.download_button(
                                label="📥 Download Notebook (.ipynb)",
                                data=jupyter_code,
                                file_name=f"analise_{selected_campaign.name}.ipynb",
                                mime="application/x-ipynb+json",
                                type="primary"
                            )

                            st.divider()

                            st.info(f"""
                            **📍 Generated Parquet File:**
                            - **Local Path:** `{filepath}`
                            - **URL:** `{base_url}/out/parquet/{filename}`
                    
                            **💡 How to use:**
                            1. Click the button above to download the notebook
                            2. Open the file in Jupyter Notebook or upload to Google Colab
                            3. Run the cells sequentially
                            4. Start your analysis!
                        
                            **🌐 To use in Google Colab:**
                            - Access: https://colab.research.google.com/
                            - Upload the downloaded .ipynb file
                            - Run the cells!
                            """)
                        else:
                            st.error("❌ Error exporting data. Check logs.")