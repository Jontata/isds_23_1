import csv
import ijson
import json
import os
import sys
sys.path.append('./DataScripts/')
import my_secrets # type: ignore

def remove_duplicates_from_csv(input_filename, output_filename):
    seen = set()
    with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Writing the header (assuming the first row is the header)
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            # Converting the row to a tuple so it's hashable
            row_tuple = tuple(row)
            if row_tuple not in seen:
                writer.writerow(row)
                seen.add(row_tuple)

# Usage
# remove_duplicates_from_csv('./WebScraper/housing_data.csv', 'housing_data_clean.csv')

def extract_advanced_subset_with_progress(input_file_path, max_elements=100):
    """
    Extracts a subset of elements from top-level lists in a very large JSON file using advanced optimizations.
    Implements progress tracking and saves the output in the provided directory for demonstration purposes.

    Parameters:
    - input_file_path (str): Path to the input JSON file.
    - max_elements (int): Maximum number of elements to extract from each list. Default is 100.

    Returns:
    - output_file_path (str): Path to the generated subset JSON file.
    """
    # Define states for our state machine
    OUTSIDE_LIST = 0
    INSIDE_LIST = 1
    INSIDE_OBJECT = 2

    state = OUTSIDE_LIST
    current_key = None
    buffer = ""
    elements_counter = 0
    object_depth = 0  # To handle nested objects

    # Determine the output file path based on the script's directory (for demonstration purposes)
    script_directory = os.path.dirname(os.path.abspath(__file__))
    base_name = os.path.basename(input_file_path).replace('.json', '_subset.json')
    output_file_path = os.path.join(script_directory, base_name)

    # Get the total size of the input file for progress tracking
    total_size = os.path.getsize(input_file_path)
    processed_size = 0
    last_percentage = 0

    with open(input_file_path, 'r') as file, open(output_file_path, 'w') as outfile:
        outfile.write("{\n")  # Start the JSON object in the output file

        # Process the file byte-by-byte
        while True:
            char = file.read(1)  # Read one byte
            if not char:
                break  # End of file

            processed_size += len(char)
            current_percentage = int((processed_size / total_size) * 100)
            if current_percentage > last_percentage:
                print(f"Processed: {current_percentage}%")
                last_percentage = current_percentage

            buffer += char

            # Detect the start of a top-level key's list
            if state == OUTSIDE_LIST and buffer.endswith('": ['):
                current_key = buffer.split('": [')[0].rsplit('"', 1)[-1]
                outfile.write(f'"{current_key}": [\n')
                elements_counter = 0
                buffer = ""
                state = INSIDE_LIST
                continue

            # If we're inside a list
            if state == INSIDE_LIST:
                # Detect the start and end of objects
                if char == '{':
                    state = INSIDE_OBJECT
                    object_depth += 1
                elif char == '}' and buffer.endswith('},'):
                    outfile.write(buffer)
                    buffer = ""
                    elements_counter += 1
                    state = INSIDE_LIST
                    # If we've reached max elements, skip the rest of the list
                    if elements_counter >= max_elements:
                        while not buffer.endswith('],'):
                            buffer += file.read(1)
                        buffer = ""
                        state = OUTSIDE_LIST

            # If we're inside an object
            elif state == INSIDE_OBJECT:
                if char == '{':
                    object_depth += 1
                elif char == '}':
                    object_depth -= 1
                    if object_depth == 0:
                        state = INSIDE_LIST

        outfile.write("]\n")  # Write the closing bracket for the last key's list
        outfile.write("}\n")  # Close the JSON object in the output file

    return output_file_path


output_path = extract_advanced_subset_with_progress(fr'{my_secrets.local_output_path_for_data}\finalfiljson1total_20230817145342.json')
print(output_path)  # This will print the path to the created subset JSON file.

"""

# Determine the output file path based on the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))
base_name = os.path.basename(input_file_path).replace('.json', '_subset.json')
output_file_path = os.path.join(script_directory, base_name)

# Write the subset to the output file
with open(output_file_path, 'w') as outfile:
    outfile.write(subset_data)

"""