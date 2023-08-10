import requests
import os
import json

def get_address_data_from_dawa(address):
    url = "https://api.dataforsyningen.dk/adresser"
    
    params = {
        "q": address,
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    response_json = response.json()

    if response.status_code == 200:
        return response_json
    else:
        print(f"Request to DAWA API failed with status code: {response.status_code}")
        return None

def get_AdresseId_from_dawa(address_input):
    data = get_address_data_from_dawa(address_input)
    return data[0]["adgangsadresse"]["id"]


if __name__ in '__main__':
    # Example usage
    address_input = "Lundegårdsvej 22, 2900 Hellerup"
    data = get_address_data_from_dawa(address_input)

    output_dir = "./tests/outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, f"DAWA_output_{address_input}.json"), "w") as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Data saved to 'outputs/DAWA_output_{address_input}.json'")
