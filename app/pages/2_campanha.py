import layouts.campaign_create
import layouts.campaign_administrate
import streamlit as st
import streamlit_antd_components as sac
import asyncio

import config.auth

config.auth.init()
# import config.db.mongo

# import config.session_state.campanha


# config.db.mongo.init()
# config.session_state.campanha.init()

if st.button("reset"):
    st.success("Reset done")

    # config.session_state.campanha.reset()

escolha = sac.segmented(
    items=[
        sac.SegmentedItem(label="Create"),
        sac.SegmentedItem(label="Manage"),
        sac.SegmentedItem(label="Delete", disabled=True),
    ],
)

match escolha:
    case "Create":
        layouts.campaign_create.render()
    case "Manage":
        layouts.campaign_administrate.render()
        # raise Exception("Opcao invalida")
    case _:
        raise Exception("Opcao invalida")
