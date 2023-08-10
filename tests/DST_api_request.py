import requests
import json
import os

def get_data_from_dst(table_id, endpoint = "/data"):
    base_url = "https://api.statbank.dk/v1"
    full_url = base_url + endpoint

    # Payload for the request
    payload = {
        "table": f"{table_id}",
        "format": "JSONSTAT",
        "valuePresentation": "Default",
        "timeOrder": "Descending"
        
        }

    response = requests.post(full_url, json=payload)  # Using POST method as we're sending a payload
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def save_to_json(data, filename):
    output_dir = "./tests/outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, f"{filename}.json"), "w") as outfile:
        json.dump(data, outfile, indent=4)

# Example usage:
"""
U27
UDDAKT60
FOLK1C
"""


table_id = "U27"  # Replace with the desired table ID
metadata = get_data_from_dst(table_id)

# Save to outputs folder
save_to_json(metadata, f"dst_extract_{table_id}")
