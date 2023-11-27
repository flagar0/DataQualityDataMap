#Uses state_code attribute to retrieve a list of cities from a given state
import requests

def fetch_cities(state_code):
    cities_url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state_code}/municipios"
    cities_data = requests.get(cities_url, verify=False).json()
    cities_list = [city['nome'] for city in cities_data]
    return cities_list