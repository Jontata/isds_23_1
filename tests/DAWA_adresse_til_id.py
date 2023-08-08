import requests
import os
import json

def get_address_id_from_dawa(address):
    url = "https://api.dataforsyningen.dk/adresser"
    
    params = {
        "q": address,
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    response_json = response.json()

    if response.status_code == 200:
        assert len(response_json) > 0 and "id" in response_json[0]
        if response_json and "id" in response_json[0]:
            return response_json[0]["id"]
        return response_json
    else:
        print(f"Request to DAWA API failed with status code: {response.status_code}")
        return None

# Example usage
address_input = "Rådmandsgade 61"
data = get_address_id_from_dawa(address_input)

output_dir = "./tests/outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(os.path.join(output_dir, f"output_{address_input}.json"), "w") as outfile:
    json.dump(data, outfile, indent=4)

print(f"Data saved to 'outputs/output_{address_input}.json'")
