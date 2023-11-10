import json
from dotenv import load_dotenv
import os

# Function to extract keys
def extract_keys(data, prefix=''):
    keys = []
    if isinstance(data, dict):
        for key in data:
            full_key = f"{prefix}{key}"
            keys.append(full_key)
            keys.extend(extract_keys(data[key], full_key + '.'))
    elif isinstance(data, list):
        if len(data) > 0:
            keys.extend(extract_keys(data[0], prefix))
        else:
            keys.append(f"{prefix}[] - Empty List")
    return keys

# Load JSON file and extract keys
def list_json_keys_to_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file:
        data = json.load(input_file)
        keys = extract_keys(data)

    with open(output_file_path, 'w') as output_file:
        for key in keys:
            output_file.write(key + '\n')

# Replace with the actual file paths
input_file_path = os.getenv('INPUT_FILE_PATH')
output_file_path = os.getenv('OUTPUT_FILE_PATH')


list_json_keys_to_file(input_file_path, output_file_path)
