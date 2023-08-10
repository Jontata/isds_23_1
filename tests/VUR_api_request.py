import requests
import my_secrets

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


def get_vur_by_vur_id(vur_id):
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

if __name__ in '__main__':
    import DAWA_api_requests, EBR_api_requests, my_base_functions
    # gather data
    target_addresse = "Lundegårdsvej 22, 2900 Hellerup"
    target_AdresseId = DAWA_api_requests.get_AdresseId_from_dawa(target_addresse)
    target_BFE = EBR_api_requests.get_BFEnr_from_HusnummerId(target_AdresseId)
    target_vur_data = get_vur_by_ejendoms_id(target_BFE)
    # save output
    my_base_functions.save_json_data(target_vur_data, f"0VUR_output_{target_addresse}.json")


