import json
import os
from dotenv import load_dotenv

load_dotenv()

def extract_media_ids(json_file, output_file):
    # Load the JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract media IDs
    media_ids = [item['data']['media']['id'] for item in data if 'media' in item['data']]

    # Save media IDs to the output file
    with open(output_file, 'w') as file:
        if output_file.endswith('.json'):
            json.dump(media_ids, file, indent=4)
        else:
            for media_id in media_ids:
                file.write(f"{media_id}\n")

# Replace with your actual file paths
json_file_path = os.getenv('INPUT_FILE_PATH')
output_file_path = os.getenv('OUTPUT_FILE_PATH')

extract_media_ids(json_file_path, output_file_path)
