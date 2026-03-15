import layouts.campaign_create
import layouts.campaign_edit
import layouts.campaign_manage
import layouts.campaign_view
import layouts.curadoria
import streamlit as st
import streamlit_antd_components as sac
import config.db.mongo

import config.auth

config.auth.init() # Login

#config.db.mongo.init() --------------- TIRAR do # se tiver dando problema

if (st.session_state.auth.cargo != "curador"):
    escolha = sac.segmented(
        items=[
            sac.SegmentedItem(label="Create"),
            sac.SegmentedItem(label="Edit"),
            sac.SegmentedItem(label="Manage"),
            sac.SegmentedItem(label="View"),
        ],
        color = 'red'
    )
else: # Secao para CURADORES
    escolha = sac.segmented(
        items=[
            sac.SegmentedItem(label="Create"),
            sac.SegmentedItem(label="Edit"),
            sac.SegmentedItem(label="Manage"),
            sac.SegmentedItem(label="View"),
            sac.SegmentedItem(label="Curation"),
        ],
        color = 'blue'
    )

if(escolha == "Create"):
    layouts.campaign_create.render()
elif(escolha == "Edit"):
    layouts.campaign_edit.render()
elif(escolha == "Manage"):
    layouts.campaign_manage.render()
elif(escolha == "View"):
    layouts.campaign_view.render()
elif (escolha == "Curation"):
    layouts.curadoria.render()
else:
    raise Exception("Opcao invalida")
