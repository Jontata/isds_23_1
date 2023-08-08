import json
import xml.etree.ElementTree as ET
import my_secrets

source_file = my_secrets.local_path_to_VUR_data
target_json_file = r"./tests/data_folder/Subset.json"
number_of_lines = 2000

def xml_to_dict(elem):
    """Converts an XML element to a Python dictionary."""
    result = {}
    for child in elem:
        child_data = xml_to_dict(child)
        if child.tag in result:
            if type(result[child.tag]) is list:
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    if not result:
        return elem.text
    return result

def extract_to_json_resilient_v2(source_file, target_file, N):
    """Extracts a subset of the XML and saves it as a JSON, while handling nested tags."""
    data = []
    bfenummer_buffer = []
    inside_bfenummer = False
    bfenummer_count = 0
    
    with open(source_file, 'r', encoding="utf-8") as fsrc:
        for line in fsrc:
            if '<BFEnummer>' in line:
                bfenummer_count += 1
                if bfenummer_count == 1:  # Start of a new main BFEnummer
                    inside_bfenummer = True

            if inside_bfenummer:
                bfenummer_buffer.append(line)
            
            if '</BFEnummer>' in line and inside_bfenummer:
                bfenummer_count -= 1
                if bfenummer_count == 0:  # End of the main BFEnummer
                    bfenummer_xml = ''.join(bfenummer_buffer)
                    try:
                        bfenummer_elem = ET.fromstring(bfenummer_xml)
                        entry = xml_to_dict(bfenummer_elem)
                        data.append(entry)
                        if len(data) >= N:
                            break
                    except ET.ParseError:
                        # Skip the problematic entry and move on
                        pass
                    bfenummer_buffer = []
                    inside_bfenummer = False

    with open(target_file, 'w', encoding="utf-8") as fdst:
        json.dump(data, fdst, ensure_ascii=False, indent=4)

    print(f"Extracted {len(data)} entries from the XML and saved to the JSON file.")

# Testing the function on the earlier formatted XML file
extract_to_json_resilient_v2(source_file, target_json_file, number_of_lines)