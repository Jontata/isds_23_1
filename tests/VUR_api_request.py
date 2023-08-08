import requests
import my_secrets
import os
import json

def get_vur_by_period():
    # Endpoint URL
    url = "https://services.datafordeler.dk/Ejendomsvurdering/Ejendomsvurdering/1/rest/HentEjendomsvurderingerAjourføringFraDatoTilDato"
    
    # Authentication details
    username = my_secrets.tjenestebruger1_usr
    password = my_secrets.tjenestebruger1_pass
    
    # Parameters for the request
    params = {
        "AjourføringDatoFra": "2023-01-01",
        "AjourføringDatoTil": "2023-02-01",
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


def get_vur_by_id(vur_id):
    # Endpoint URL
    url = "https://services.datafordeler.dk/Ejendomsvurdering/Ejendomsvurdering/1/rest/HentEjendomsvurderingerForEjendomsvurderingId"
    
    # Authentication details
    username = my_secrets.tjenestebruger1_usr
    password = my_secrets.tjenestebruger1_pass
    
    # Parameters for the request
    params = {
        "id": vur_id,
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


def get_vur_by_ejendoms_id(BFEnummer):
    # Endpoint URL
    url = "https://services.datafordeler.dk/Ejendomsvurdering/Ejendomsvurdering/1/rest/HentEjendomsvurderingerForBFE"
    
    # Authentication details
    username = my_secrets.tjenestebruger1_usr
    password = my_secrets.tjenestebruger1_pass
    
    # Parameters for the request
    params = {
        "BFEnummer": BFEnummer,
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


# Test the function with the provided address ID
address_id_input = "6022778"
data = get_vur_by_ejendoms_id(address_id_input)

# Save the JSON output to a file in the "outputs" subfolder
output_dir = "./tests/outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(os.path.join(output_dir, f"output_vur_egendomsid_{address_id_input}_data.json"), "w") as outfile:
    json.dump(data, outfile, indent=4)

print(f"Data saved to 'outputs/output_vur_{address_id_input}.json'")
