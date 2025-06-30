import streamlit as st
from pymongo import MongoClient
from bunnet import init_bunnet

from schemas import Campaign


def init():
    st.session_state.mongo_client = MongoClient("mongodb+srv://publico:123@cluster0.hijrd3t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
