import streamlit as st
from pymongo import MongoClient
from bunnet import init_bunnet

from schemas import Campaign


def init():
    if "mongo_client" not in st.session_state:
        # st.session_state.mongo_connection_init = True
        # var_host = "Host"
        # var_port = 18378 TROCAR MEU LOGIN E USUARIO PELOS INSERIDOS
        st.session_state.mongo_client = MongoClient("mongodb+srv://flaviomidea:flavio@cluster0.hijrd3t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        # init_bunnet(database=client.newbase, document_models=[Campaign])
