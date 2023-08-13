import requests
import my_secrets
import DAWA_api_requests
import os
import json

# Authentication details
username = my_secrets.tjenestebruger1_usr
password = my_secrets.tjenestebruger1_pass

def BRR_BFE_to_basics(BFE_number):
    url = "https://services.datafordeler.dk/BBR/BBRPublic/1/REST/enhed"
    
    # Parameters for the request
    params = {
        "BFENummer": BFE_number,
        "username": username,
        "password": password,
        "format": "JSON"
    }

    # Make the request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code: {response.status_code}"}

def get_unit_by_address(address_id):
    # Endpoint URL
    url = "https://services.datafordeler.dk/BBR/BBRPublic/1/rest/enhed"
    
    # Parameters for the request
    params = {
        "AdresseIdentificerer": address_id,
        "username": username,
        "password": password
    }
    
    # Headers for the request
    headers = {
        "Accept": "application/json"
    }
    
    # Make the request
    response = requests.get(url, params=params, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code: {response.status_code}"}


def get_BBR_data_from_DAR_ID(DAR_ID):
    url = "https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bygning"
    params = {
        "husnummer": DAR_ID,
        "username": username,
        "password": password
    }

    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code: {response.status_code}"}


if __name__ in '__main__':
    import my_base_functions
    #target_address = "Mosebakken 19c"
    target_address = "Lundegårdsvej 22, 2900 Hellerup"
    #target_address = "Vedbæk Strandvej 322, 2950 Vedbæk"
    DAR_data = DAWA_api_requests.get_address_data_from_dawa(target_address)
    DAR_data_ID = DAR_data[0]["adgangsadresse"]["id"]
    data = get_BBR_data_from_DAR_ID(DAR_data_ID)

    # save
    my_base_functions.save_json_data(DAR_data, f"0_DAR_output_{target_address}_data.json")
    my_base_functions.save_json_data(data, f"0_BRR_output_{target_address}_data.json")