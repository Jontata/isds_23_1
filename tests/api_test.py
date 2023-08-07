import requests
import my_secrets

# Replace these with your own details
username = my_secrets.tjenestebruger1_usr
password = my_secrets.tjenestebruger1_pass


building_id = 'EAID_F8196C58_7115_48a6_9A1D_B49BC0F6289A'
registration_from = 'your_registration_from_date'
registration_to = 'your_registration_to_date'

url = f'https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bbrsag?Bygning={building_id}&&username={username}&password={password}'

response = requests.get(url)

# Check the status code and print the response
if response.status_code == 200:
    print(response.json())
else:
    print(f'Request failed with status code {response.status_code}')
