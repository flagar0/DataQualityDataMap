import streamlit as st
import pandas as pd
import pymongo
import datetime
import config.db.mongo
from schemas import Campaign,Dataquality,Headers
import json
import xarray # INSTALAR NETCDF4, SPICY
import streamlit_antd_components as sac
import bunnet as bn
from streamlit_timeline import st_timeline
from time import sleep
from stqdm import stqdm
from config.functions import *
from streamlit_extras import stateful_button as stb

user_id = "a"

colors = {
        'yellow': '#FFFF00',
        'white': '#F3F3F3',
        'black': '#000000'
    }

next_year = 2024
jan_1 = datetime.date(2012, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)



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
    df = df.reset_index() # Retira o index para nao perde-lo
    payload = df.to_dict(orient="records")
    print("Inserindo na tabela")
    dez_porcento = int(len(payload)*0.1)
    num = 0
    resto = int(len(payload)%0.1)

    for i in stqdm(range(dez_porcento,int(len(payload)-resto+1),dez_porcento)):
        print(num)
        #result = coll.insert_one(i)
        result = coll.insert_many(payload[i-dez_porcento:i])
        print(f"{i-dez_porcento} : {i}")
        num += dez_porcento
    if resto != 0:
        result2 = coll.insert_many(payload[len(payload)-resto:resto])
        num += resto
    return num


def generate_dataquality(df):
    #Colocar explicacao
    #Limpa os cabecalhos - Tira cabecalhos de tempo
    headers = list(df.columns.values)

    try:
        #headers.remove('base_time')
        #headers.remove('time_offset')
        headers.remove('time')
    except:
        print("Sem cabecalhos de Tempo!", headers[0])

    analysis = dict()

    for header in headers:
        isna = pd.isna(df[header])
        green = []
        red = []
        old_time = df['time'][0]
        first_red=None

        for i in range(1, len(df) - 1):  # 2014-09-01 00:12:32
            if (isna[i] == True):  # eh nulo
                if(str(old_time) != str(df['time'][i]) ):
                    green.append({"start": str(old_time), "end": str(df['time'][i]), "style": "background-color: green;"})

                if(isna[i+1]==True):
                    if(first_red==None): first_red=df['t'][i]
                else:
                    if(first_red==None):
                        red.append({"start": str(df['time'][i]), "end": str(df['time'][i + 1]),"style": "background-color: red;"})
                    else:
                        red.append({"start": str(first_red), "end": str(df['time'][i + 1]),"style": "background-color: red;"})
                        first_red=None

                old_time = str(df['time'][i + 1])
        if(first_red==None): # termina com uma verde
            green.append({"start": str(old_time), "end": str(df['time'][len(df) - 1]), "style": "background-color: green;"})
        else:
            red.append({"start": str(first_red), "end": str(df['time'][len(df) - 1]), "style": "background-color: red;"})
        analysis.update({header:{"green":green,"red":red,"yellow":[],"white":[],"black":[],"note":None}})
    return analysis

def upload_dataquality(data_quality,selected_campaign):
    try:
        client = st.session_state.mongo_client
        user = st.session_state.auth.user
        bn.init_bunnet(database=client[user], document_models=[Dataquality])
        dq = Dataquality(
                name=selected_campaign.name,
                user_id=selected_campaign.user_id,
                collection_id=selected_campaign.collection_id,
                data=data_quality
            )
        dq.insert()
        return True #BaseException as e
    except:
        return False

def render():
    st.session_state.table_data = st.session_state.get("table_data", [])
    if 'data_quality' not in st.session_state :  st.session_state.data_quality = []
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
        tables = pd.DataFrame(
            st.session_state.table_data,
            columns=["name", "description", "date"],
        )
        st.dataframe(
            data=tables,
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

        uploaded_file = st.file_uploader("Choose a CSV file",accept_multiple_files=True, type=["csv", "tsv", "cdf", "nc"])
        df = None
        variables = None
        if len(uploaded_file) != 0:
            st.info("File uploaded successfully!")
            print(uploaded_file[0].name[-3:])

            #Possivel erro: colocar mais de um tipo de arquivo juntos
            if (uploaded_file[0].name[-3:] == "csv"):  # .csv
                df = pd.concat((pd.read_csv(f, sep=None) for f in uploaded_file), ignore_index=True)

            elif (uploaded_file[0].name[-3:] == "tsv"):  # .tsv
                df = pd.concat((pd.read_csv(f, sep='\t') for f in uploaded_file), ignore_index=True)

            elif (uploaded_file[0].type == "application/x-netcdf" or uploaded_file[0].type == "application/vnd.wolfram.cdf" ):  # .cdf
                variables = xarray.open_dataset(uploaded_file[0]).variables # pega as informacoes de cabecalho do primeiro
                df = pd.concat((xarray.open_dataset(f).to_pandas() for f in uploaded_file))#, ignore_index=True)#xarray.open_dataset(uploaded_file).to_pandas()

        if st.session_state.data_quality == [] and df is not None :
            try:
                st.session_state.data_quality = generate_dataquality(df)
            except (RuntimeError, TypeError, NameError) as e:
                print("Erro ao gerar dataquality")
                print(e)
            print("salvei por cima")
        st.divider()  # ------------------
        escolha = sac.segmented(
            items=[
                sac.SegmentedItem(label="Preview Data"),
                sac.SegmentedItem(label="Add Data Quality Report"),
            ],)



        if(escolha=="Preview Data"):
            print(df)
            if(df is not None ): st.write(df.head(5))
            if (df is not None): st.write(df.tail(5))

        elif(escolha=="Add Data Quality Report"):
            st.markdown(
                '<div style="display: block ruby;"> <div style="background-color: #FFFF00; width: 15px; height: 15px; padding-right:2px;"></div> Suspect </div>'
                '<div style="display: block ruby;"> <div style="background-color: #F3F3F3; width: 15px; height: 15px; padding-right:2px;"></div> Note </div>'
                '<div style="display: block ruby;"> <div style="background-color: black; width: 15px; height: 15px; padding-right:2px;"></div> Incorrect </div>',
                unsafe_allow_html=True
            )
            selected_color = st.selectbox("Select a quality level", list(colors.keys()))
            # Data Quality


            data_quality= st.session_state.data_quality

            if selected_color:
                st.markdown(
                    f'<div style="background-color: {colors[selected_color]}; width: 50px; height: 50px;"></div>',
                    unsafe_allow_html=True
                )
            st.write(f'Selected quality: {selected_color}')

            if(selected_color == "white"):
                note_disabled = False
            else:
                note_disabled = True
            note = st.text_area(label="Note",disabled=note_disabled )
            date = st.date_input(
                "Select the period of data collection",
                (jan_1, datetime.date(next_year, 1, 7)),
                jan_1,
                dec_31,
                format="MM.DD.YYYY",# 2014-09-01 00:12:32
            )
            hour_min = st.time_input("Start time",step=60)
            hour_max = st.time_input("End time", step=60)

            start_datetime = datetime.datetime.combine(date[0], hour_min)
            end_datetime = datetime.datetime.combine(date[1],hour_max)


            st.divider()#------------------
            st.subheader("Preview Timeline")

            if (data_quality !=None):
                analise = st.selectbox("Select Data", options=list(data_quality))
                items = []
                for g in data_quality[analise]["green"]:  # verdes
                    items.append(g)
                for r in data_quality[analise]["red"]:
                    items.append(r)
                for y in data_quality[analise]["yellow"]:
                    items.append(y)
                for w in data_quality[analise]["white"]:
                    items.append(w)
                for b in data_quality[analise]["black"]:
                    items.append(b)



                items_new = items
                col_prev, col_add = st.columns(2)
                bool_add_btn = True
                with col_prev:
                    if (st.button("Preview")):  # "style": "background-color: selected color;"
                        items_new.append({"start": str(start_datetime), "end": str(end_datetime), "style": "background-color: "+colors[selected_color]+";"})
                        bool_add_btn = False
                with col_add:
                    if (st.button("Add",disabled=bool_add_btn)):
                        data_quality[analise][selected_color].append({"start": str(start_datetime), "end": str(end_datetime), "style": "background-color: "+colors[selected_color]+";"})
                        items_new.append({"start": str(start_datetime), "end": str(end_datetime),
                                          "style": "background-color: " + colors[selected_color] + ";"})
                        if(note != ""):
                            data_quality[analise]["note"] = note
                        st.session_state.data_quality = data_quality
                if (st.button("Clear")):
                    bool_add_btn = True

                timeline = st_timeline(items_new, groups=[], options={
                "snap": None,
                "stack": False,
                "selectable": False,
                })
                if (note != ""):
                    st.markdown(
                        f'<div style="diplay: -webkit-box;"> <div style="background-color: #FFFF; width: 15px; height: 15px; padding-right:2px;"></div> Note: {note}</div>',
                        unsafe_allow_html=True
                    )

            else:
                st.warning("Error: You need add a data")
        else:
            pass
            #raise Exception("Invalid Option")
        if selected_campaign:
            if stb.button("Submit data", key="btn_data"):


                if upload_dataquality(st.session_state.data_quality, selected_campaign):
                    st.success(
                        f"Data Quality Added Successfully to Campaign {selected_campaign.name}"
                    )
                    st.session_state.data_quality = []

                if upload_headers(variables,df.columns,selected_campaign):
                    st.success(
                        f"Headers Variables Added Successfully to Campaign {selected_campaign.name}"
                    )
                else:
                    st.error(
                        f"Error on add headers variables to Campaign {selected_campaign.name}"
                    )

                number_of_collections = mongoimport(
                    df,
                    user,
                    # "newcollection",
                    selected_campaign.collection_id,
                )

                st.success(
                        f"Data Added Successfully to Campaign {selected_campaign.name}! It now has {number_of_collections} documents associated with it"
                    )
