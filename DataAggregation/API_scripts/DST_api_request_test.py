import requests
import json

BASE_URL = 'https://api.statbank.dk/v1'

def get_tableinfo_from_dst(table_id, endpoint='/tableinfo'):
    params = {
        'id': table_id,
        'format': 'JSON'
    }
    response = requests.get(BASE_URL + endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching table info for table {table_id}. Status Code: {response.status_code}")
        print(response.content)
        return None
    
def get_data_from_dst(table_id, request_format='csv'):
    variables_info = get_tableinfo_from_dst(table_id)['variables']
    if not variables_info:
        raise Exception("Failed to fetch table information.")
        
    variable_ids = [var['id'] for var in variables_info]
    
    variables_list = []
    for variable_id in variable_ids:
        if variable_id == 'OMRÅDE':
            values = ['155', '01', '101', '147']
        else:
            values = ['*']
        variable_entry = {'code': variable_id, 'values': values}
        variables_list.append(variable_entry)
    
    params = {
        'table': table_id,
        'format': request_format,
        'variables': variables_list
    }
    response = requests.post(BASE_URL + '/data', json=params)
    if response.status_code == 200:
        return response.text, params
    else:
        print(f"Error fetching data for table {table_id}. Status Code: {response.status_code}")
        raise Exception(response.content)

# Initialize last_params before the try block
last_params = {}

# Testing the function
try:
    result_data, last_params = get_data_from_dst("INDKP106", request_format='BULK')
    print("Successfully fetched data. Preview:")
    print(result_data[:500])  # Displaying the first 500 characters of the data for verification
except Exception as e:
    print("Failed to fetch data!")
    print("Error:", e)
    if last_params:  # Only print last_params if it has been populated
        print("\nLast request sent:")
        print(json.dumps(last_params, indent=4))
    print("\nError Response:")
    print(e)  # Printing the error message (which is the server's response content in case of a data fetch failure)

