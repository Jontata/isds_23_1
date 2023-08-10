import requests
import my_secrets
import os
import json

# Authentication details
username = my_secrets.tjenestebruger1_usr
password = my_secrets.tjenestebruger1_pass

def get_EBR_data_from_HusnummerId(HusnummerId_input):
    url = "https://services.datafordeler.dk/EBR/Ejendomsbeliggenhed/1/rest/BFEnrAdresse"
    
    params = {
        "HusnummerId": HusnummerId_input,
        "username": username,
        "password": password
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code: {response.status_code}"}

def get_BFEnr_from_HusnummerId(DAR_data_ID):
    data = get_EBR_data_from_HusnummerId(DAR_data_ID)
    return data["features"][0]["properties"]["bestemtFastEjendomBFENr"]


if __name__ in '__main__':
    import my_base_functions
    import DAWA_api_requests
    example_target_address = "Lundegårdsvej 22, 2900 Hellerup"
    DAR_data = DAWA_api_requests.get_address_data_from_dawa(example_target_address)
    DAR_data_ID = DAR_data[0]["adgangsadresse"]["id"]
    print(DAR_data_ID)
    EBR_data = get_EBR_data_from_HusnummerId(DAR_data_ID)
    print(EBR_data)
    my_base_functions.save_json_data(EBR_data, f"0_EBR_{example_target_address}.json")
    try:
        print(EBR_data["features"][0]["properties"]["bestemtFastEjendomBFENr"])
    except:
        pass
