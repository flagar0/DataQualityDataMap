import layouts.campaign_viewpublic
import streamlit as st
import streamlit_antd_components as sac
import config.db.mongo

import config.auth as Autenticacao

config.db.mongo.init() #--------------- TIRAR do # se tiver dando problema

if "auth" not in st.session_state:
    st.session_state.auth = Autenticacao.Auth()

st.session_state.auth.user = "publico"
st.session_state.auth.is_authenticated = True
st.session_state.auth.public = True

layouts.campaign_viewpublic.render()

