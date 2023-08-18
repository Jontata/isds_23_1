import os
import my_secrets
import pandas as pd

data_location = my_secrets.local_output_path_for_data
dst_location = my_secrets.local_path_for_dst_data

#! DST Population data
file_name = "FOLK1C_export_2023-08-14.csv"
file_path = f"{dst_location}/{file_name}" #? this is a very large file
subset = pd.read_csv(file_path, delimiter=';', nrows=1000) #? load the first thousand rows
print(subset)

#! VUR data




#! BRR data





"""
#? Code to explore directory

files_and_subdirectories = os.listdir(dst_location)

for item in files_and_subdirectories:
    print(item)

    

with open(file_path, 'r') as f:
    lines = f.readlines()
    print(lines[41])  # since line numbers start from 1 and list indices from 0
"""