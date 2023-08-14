import os
import json
import openpyxl
import csv

def save_to_json(json_object, file_name, output_dir = "./DataScripts/outputs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, f"{file_name}.json"), "w") as outfile:
        json.dump(json_object, outfile, indent=4)
    print(f"Data saved to '{output_dir}/{file_name}'")

def save_to_xlsx(data, filename, output_dir = "./DataScripts/outputs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, f"{filename}.xlsx"), "wb") as outfile:
        outfile.write(data)

def save_to_csv(data, filename, output_dir = "./DataScripts/outputs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, f"{filename}.csv"), "w", newline='', encoding='utf-8-sig') as outfile:
        outfile.write(data)