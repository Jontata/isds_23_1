import os
import json

def save_json_data(json_object, file_name, output_dir = "./tests/outputs"):
    if file_name[-5:] != '.json':
        file_name = file_name + ".json"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, file_name), "w") as outfile:
        json.dump(json_object, outfile, indent=4)
    print(f"Data saved to '{output_dir}/{file_name}'")
