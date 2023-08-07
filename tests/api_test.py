import requests
import my_secrets

# Replace these with your own details
username = my_secrets.tjenestebruger1_usr
password = my_secrets.tjenestebruger1_pass


building_id = '0a3f50ad-9b51-32b8-e044-0003ba298018'
registration_from = 'your_registration_from_date'
registration_to = 'your_registration_to_date'

url = f'https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bbrsag?Bygning={building_id}&&username={username}&password={password}'

response = requests.get(url)

# Check the status code and print the response
if response.status_code == 200:
    print(response.json())
else:
    print(f'Request failed with status code {response.status_code}')
