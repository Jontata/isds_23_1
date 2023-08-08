import requests
import my_secrets
from DAWA_adresse_til_id import get_address_id_from_dawa
import os
import json


def get_unit_by_address(address_id):
    # Endpoint URL
    url = "https://services.datafordeler.dk/BBR/BBRPublic/1/rest/enhed"
    
    # Authentication details
    username = my_secrets.tjenestebruger1_usr
    password = my_secrets.tjenestebruger1_pass
    
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

# Test the function with the provided address ID
address_id_input = get_address_id_from_dawa("Rådmandsgade 61, 520, København")
data = get_unit_by_address(address_id_input)

# Save the JSON output to a file in the "outputs" subfolder
output_dir = "./tests/outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(os.path.join(output_dir, f"output_{address_id_input}_data.json"), "w") as outfile:
    json.dump(data, outfile, indent=4)

print(f"Data saved to 'outputs/output_{address_id_input}.json'")
