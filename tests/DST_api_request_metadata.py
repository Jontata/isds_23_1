import requests
import json
import os

def get_table_metadata(tableID, lang="en"):
    base_url = "https://api.statbank.dk/v1"
    endpoint = f"/tableinfo/{tableID}?lang={lang}"
    full_url = base_url + endpoint

    response = requests.get(full_url)
    
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
table_id = "U37"  # Replace with the desired table ID
metadata = get_table_metadata(table_id)

# Save to outputs folder
save_to_json(metadata, f"dst_metadata_{table_id}")
