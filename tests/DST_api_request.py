import requests

def get_metadata_from_dst(tableID, lang="en"):
    base_url = "https://api.statbank.dk/v1"
    endpoint = f"/data/tableinfo/{tableID}?lang={lang}"
    full_url = base_url + endpoint
    response = requests.get(full_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_data_from_dst(tableID, format="JSONSTAT", lang="en"):
    base_url = "https://api.statbank.dk/v1"
    endpoint = f"/data/{tableID}/{format}?lang={lang}"
    full_url = base_url + endpoint

    response = requests.get(full_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example usage:
data = get_metadata_from_dst("FOLK1A")
print(data)
