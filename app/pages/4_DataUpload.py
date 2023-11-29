import layouts.data_upload
import streamlit as st
import streamlit_antd_components as sac

import config.auth

# config.auth.init()
# import config.db.mongo

# import config.session_state.campanha


# config.db.mongo.init()
# config.session_state.campanha.init()

if st.button("reset"):
    st.success("Reset done")

    # config.session_state.campanha.reset()

layouts.data_upload.render()
