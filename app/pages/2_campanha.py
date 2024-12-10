import layouts.campaign_create
import layouts.campaign_edit
import layouts.campaign_manage
import layouts.campaign_view
import streamlit as st
import streamlit_antd_components as sac
import config.db.mongo

import config.auth

config.auth.init() # Login

#config.db.mongo.init() --------------- TIRAR do # se tiver dando problema


if st.button("reset"):
    st.success("Reset done")

    # config.session_state.campanha.reset()

escolha = sac.segmented(
    items=[
        sac.SegmentedItem(label="Create"),
        sac.SegmentedItem(label="Edit"),
        sac.SegmentedItem(label="Manage"),
        sac.SegmentedItem(label="View"),
    ],
)

if(escolha == "Create"):
    layouts.campaign_create.render()
elif(escolha == "Edit"):
    layouts.campaign_edit.render()
elif(escolha == "Manage"):
    layouts.campaign_manage.render()
elif(escolha == "View"):
    layouts.campaign_view.render()
else:
    raise Exception("Opcao invalida")
