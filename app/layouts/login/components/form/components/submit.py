import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
#from config.auth import Auth


def exec():
    auth: Auth = st.session_state.auth
    client = MongoClient("mongodb+srv://{user}:{password}@cluster0.hijrd3t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(user=st.session_state["auth_email_input"], password=st.session_state["auth_pwd_input"]),timeoutMS=0)

    try:
        if client.admin.command('ismaster')['ismaster']:

            if ("mongo_client" not in st.session_state) or st.session_state.auth.public:
                st.session_state.mongo_client = client
                auth.is_authenticated = True
                st.session_state.auth.public = False
                auth.user = st.session_state["auth_email_input"]
                st.success(body="Sucessfull Logged")

    except OperationFailure:
        st.error(body="Error on Login. Database not found.")
    except ServerSelectionTimeoutError:
        st.error(body="Error on Login. MongoDB Server is down.")


