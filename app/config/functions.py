import streamlit as st
import pandas as pd
import pymongo
import config.db.mongo
from schemas import Campaign,Dataquality,Headers
import config.db.mongo
from schemas import Campaign
import json
import streamlit_antd_components as sac
import numpy as np
import ast
import bunnet as bn
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_timeline import st_timeline
import zipfile
import io
from pygwalker.api.streamlit import StreamlitRenderer

# def get_campaigns_by_user(user):
#     client = st.session_state.mongo_client
#
#     bn.init_bunnet(database=client.info, document_models=[Campaign])
#     result = Campaign.find({"user_id":user}).to_list()
#     return result
#@st.cache_resource
def mongoexport(df, db_name, coll_name): # USANDO PYMONGO
    """Export a panda file from a mongo colection
    returns: panda data
    """
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db[coll_name]
    return pd.DataFrame(list(coll.find(projection={'_id': False}))) ## tirar o _id e limita para nao travar

def get_camaign_names(df,x_axis,y_axis):
    return sns.lineplot(data=df, x=x_axis, y=y_axis, markers=True)


def get_campaign_dq(db_name, id): # data quality
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db["Dataquality"]
    return pd.DataFrame(list(coll.find({"collection_id": id},projection={'_id': False}, limit=0)))  ## tirar o _id e limita para nao travar

def get_campaigns_by_user(user):
    client = st.session_state.mongo_client
    user = st.session_state.auth.user
    bn.init_bunnet(database=client.info, document_models=[Campaign])
    result = Campaign.find({"user_id":user}).to_list()

    return result

def delete_campaign(delete,collection_id):
    client = st.session_state.mongo_client
    user = st.session_state.auth.user
    db = client[user]
    db.drop_collection(collection_id)

    bn.init_bunnet(database=client[user], document_models=[Headers.Headers])
    Headers.Headers.find(Headers.Headers.name == delete).delete().run()

    bn.init_bunnet(database=client[user], document_models=[Dataquality])
    Dataquality.find(Dataquality.name == delete).delete().run()

    bn.init_bunnet(database=client.info, document_models=[Campaign])
    Campaign.find_one(Campaign.name == delete).delete().run()

def get_header(db_name, id):
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db["Headers"]
    return pd.DataFrame(coll.find({"collection_id": id},projection={'_id': False}, limit=0))['header'][0]  ## tirar o _id e limita para nao travar

def upload_header(header,selected_campaign):
    if(header != None):
        client = st.session_state.mongo_client
        user = st.session_state.auth.user
        bn.init_bunnet(database=client[user], document_models=[Headers.Headers])
        dq = Headers.Headers(
                name=selected_campaign.name,
                user_id=selected_campaign.user_id,
                collection_id=selected_campaign.collection_id,
                header=header
            )
        dq.insert()
        return True #BaseException as e


def update_dataquality(data_quality,selected_campaign):
    try:
        client = st.session_state.mongo_client
        user = st.session_state.auth.user
        db = client[user]
        coll = db["Dataquality"]
        coll.update_one({"collection_id": selected_campaign}, {"$set": {"data": data_quality}})
        return True #BaseException as e
    except BaseException as e:
        print(e)
        return False

@st.cache_data
def download_campaign(_ds,ds_hd,tipo,range,user,campaign):

    for i in ds_hd.keys():
        _ds[i].attrs.update(ast.literal_eval(ds_hd[i]))  # .encode('utf-8'))

    # for var in _ds.variables:
    #     _ds[var].encoding.clear()

    memoria = io.BytesIO()
    compressao = dict(zlib=True, complevel=5)
    with zipfile.ZipFile(memoria, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for dia, dataset in _ds.groupby("time.date"):
            if(dia >= range[0] and dia <= range[1]):
                if(tipo==".csv"):
                    pandas = dataset.to_pandas()
                    nome = f"{user}_{campaign}_{str(dia)}.csv"# USUARIO_CAMPANHA_DATA
                    arq = pandas.to_csv().encode('utf-8')
                elif(tipo==".cdf"):
                    #encoding = {var: compressao for var in dataset.data_vars}
                    nome = f"{user}_{campaign}_{str(dia)}.cdf"
                    arq =  dataset.to_netcdf()
                elif(tipo==".nc"):
                    #encoding = {var: compressao for var in dataset.data_vars}
                    nome = f"{user}_{campaign}_{str(dia)}.nc"
                    arq= dataset.to_netcdf()

                zf.writestr(nome, arq)
    return memoria.getvalue()

def upload_headers(variables,_columns,_selected_campaign):

    headers = {}
    for i in _columns:
        if (variables != None):
            headers.update({i: str(variables.mapping[i].attrs)})
        else:
            headers.update({i: "{}"})

    try:
        client = st.session_state.mongo_client
        user = st.session_state.auth.user
        bn.init_bunnet(database=client[user], document_models=[Headers.Headers])
        dq = Headers.Headers(
            name=_selected_campaign.name,
            user_id=_selected_campaign.user_id,
            collection_id=_selected_campaign.collection_id,
            header=headers
        )
        dq.insert()
        return True
    except BaseException as e:
        print(e)
        return False
