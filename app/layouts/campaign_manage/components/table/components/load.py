import streamlit as st
import pandas as pd
import pymongo
import datetime
import config.db.mongo
from schemas import Campaign
import json
import xarray # INSTALAR NETCDF4, SPICY
import streamlit_antd_components as sac
from schemas import Dataquality
import bunnet as bn

from time import sleep

from streamlit_extras import stateful_button as stb

user_id = "a"

colors = {
        'Amarelo': '#FFFF00',
        'Branco': '#FFFFFF',
        'Preto': '#000000'
    }

next_year = 2024
jan_1 = datetime.date(2015, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

def get_campaigns_by_user(user):
    client = st.session_state.mongo_client

    bn.init_bunnet(database=client.newbase, document_models=[Campaign])
    result = Campaign.find_all().to_list()

    return result


# def create_new_campaigncollection(campaign_id):
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = myclient["newbase"]

#     mycol = mydb[campaign_id]

#     return


# def mongoimport(csv_path, db_name, coll_name, db_url='localhost', db_port=27000):
# def mongoimport(csv_path, db_name, coll_name):
def mongoimport(df, db_name, coll_name):
    """Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection
    """
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db[coll_name]
    # data = pd.read_csv(csv_path)
    payload = df.to_dict(orient="records")

    # coll.delete_many()
    coll.insert_many(payload)
    return coll.estimated_document_count()


def delete_campaign(delete):
    client = st.session_state.mongo_client

    bn.init_bunnet(database=client.newbase, document_models=[Campaign])

    Campaign.find_one(Campaign.name == delete).delete()

def generate_dataquality(df):
    #Colocar explicacao
    #Limpa os cabecalhos - Tira cabecalhos de tempo
    headers = list(df.columns.values)

    try:
        headers.remove('base_time')
        headers.remove('time_offset')
    except:
        print("Sem cabecalhos de Tempo!", headers[0])

    analysis = dict()

    for header in headers:
        isna = pd.isna(df[header])
        green = []
        red = []
        old_time = df['time_offset'][0]
        first_red=None

        for i in range(1, len(df) - 1):  # 2014-09-01 00:12:32
            if (isna[i] == True):  # eh nulo
                if(str(old_time) != str(df['time_offset'][i]) ):
                    green.append({"start": str(old_time), "end": str(df['time_offset'][i]), "style": "background-color: green;"})

                if(isna[i+1]==True):
                    if(first_red==None): first_red=df['time_offset'][i]
                else:
                    if(first_red==None):
                        red.append({"start": str(df['time_offset'][i]), "end": str(df['time_offset'][i + 1]),"style": "background-color: red;"})
                    else:
                        red.append({"start": str(first_red), "end": str(df['time_offset'][i + 1]),"style": "background-color: red;"})
                        first_red=None

                old_time = str(df['time_offset'][i + 1])
        if(first_red==None): # termina com uma verde
            green.append({"start": str(old_time), "end": str(df['time_offset'][len(df) - 1]), "style": "background-color: green;"})
        else:
            red.append({"start": str(first_red), "end": str(df['time_offset'][len(df) - 1]), "style": "background-color: red;"})
        analysis.update({header:{"green":green,"red":red}})
    return analysis

def upload_dataquality(data_quality,selected_campaign):
    client = st.session_state.mongo_client
    bn.init_bunnet(database=client.newbase, document_models=[Dataquality])
    user = st.session_state.auth.user
    dq = Dataquality(
            name=selected_campaign.name,
            user_id=selected_campaign.user_id,
            collection_id=selected_campaign.collection_id,
            data=data_quality
        )
    dq.insert()
    return True #BaseException as e

def render():
    st.session_state.table_data = st.session_state.get("table_data", [])

    # TO-DO inicializar table_data com None
    # TO-DO trocar nome table_data para campaing list

    user = st.session_state.auth.user
    user_campaigns_list = get_campaigns_by_user(user)

    st.session_state.table_data = []
    for campaign in user_campaigns_list:
        Campaign_name = campaign.name
        description = campaign.description
        date = campaign.date

        st.session_state.table_data.append((Campaign_name, description, date))

    if st.session_state.table_data:
        df = pd.DataFrame(
            st.session_state.table_data,
            columns=["name", "description", "date"],
        )
        st.dataframe(
            data=df,
            hide_index=True,
            column_order=["name", "description", "date"],
            column_config={
                "name": st.column_config.TextColumn(label="Name"),
                "description": st.column_config.TextColumn(label="Description"),
                "date": st.column_config.TextColumn(label="Date"),
            },
        )

        selected_campaign = st.selectbox(
            label="Select a campaign to manage",
            options=user_campaigns_list,
            index=None,
            format_func=lambda x: x.name
        )

        escolha = sac.segmented(
            items=[
                sac.SegmentedItem(label="Add Data"),
                sac.SegmentedItem(label="Add Data Quality Report"),
            ],
        )

        if(escolha=="Add Data"):
            uploaded_file = st.file_uploader("Choose a CSV file", type=["csv","tsv","cdf",".nc"])
            if uploaded_file is not None:
                st.info("File uploaded successfully!")
                print(uploaded_file.type)
                if(uploaded_file.type=="text\csv"): #.csv
                    df = pd.read_csv(uploaded_file)

                elif(uploaded_file.type=="text/tab-separated-values"):#.tsv
                    df = pd.read_csv(uploaded_file,sep='\t')

                elif(uploaded_file.type=="application/x-netcdf"):#.cdf
                    df =  xarray.open_dataset(uploaded_file).to_pandas()

                st.subheader("Data Preview")
                st.write(df.head(10))

                # Data Quality
                data_quality = generate_dataquality(df)

                if selected_campaign:
                    if stb.button("Submit data", key="btn_data"):
                        # number_of_collections = mongoimport(
                        #         df,
                        #         "newbase",
                        #         # "newcollection",
                        #         selected_campaign.collection_id,
                        #     )
                        print(upload_dataquality(data_quality, selected_campaign))
                        # st.success(
                        #         f"Data Added Successfully to Campaign {selected_campaign.name}! It now has {number_of_collections} documents associated with it"
                        #     )
                        sleep(2)
                        #st.rerun()

        elif(escolha=="Add Data Quality Report"):
            selected_color = st.selectbox("Select a quality level", list(colors.keys()))

            if selected_color:
                st.markdown(
                    f'<div style="background-color: {colors[selected_color]}; width: 50px; height: 50px;"></div>',
                    unsafe_allow_html=True
                )
            st.write(f'Selected quality: {selected_color}')
            d = st.date_input(
                "Select the period of data collection",
                (jan_1, datetime.date(next_year, 1, 7)),
                jan_1,
                dec_31,
                format="MM.DD.YYYY",
            )
        else:
            raise Exception("Invalid Option")

