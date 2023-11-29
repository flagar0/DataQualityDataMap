import layouts.campaign_create
import layouts.campaign_edit
import layouts.campaign_manage
import streamlit as st
import streamlit_antd_components as sac
import config.db.mongo

import config.auth

config.auth.init()

config.db.mongo.init()

# config.auth.init()
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
        sac.SegmentedItem(label="Edit"),
        sac.SegmentedItem(label="Manage"),
    ],
)

match escolha:
    case "Create":
        layouts.campaign_create.render()
    case "Edit":
        layouts.campaign_edit.render()
    case "Manage":
        layouts.campaign_manage.render()
        # raise Exception("Opcao invalida")
    case _:
        raise Exception("Opcao invalida")
