import streamlit as st
import requests
import utils.ibge

def render ():
    
    # Retrieve or initialize the table data from cache
    table_data = st.session_state.get("table_data", [])

    # Retrieve state data from ibge API
    state_url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    state_data = requests.get(state_url, verify=False).json()

    # Retrive states names
    state_options = []
    for state in state_data:
        state_options.append(state['nome']) #Could use list compreheension

    state_options=sorted(state_options) 

    selected_state = st.selectbox("Selecione seu estado", state_options, index=0)

    selected_state_code = [state['sigla'] for state in state_data if state['nome'] == selected_state][0]

    #Retrieve cities names based on states (it must use state abbreviation for the URL)
    cities_list = sorted(utils.ibge.fetch_cities(selected_state_code))
    selected_city = st.selectbox("Selecione sua cidade", cities_list, index=0)

    return selected_state, selected_city
