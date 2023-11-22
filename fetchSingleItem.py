import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Blizzard API credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Get an access token
token_url = "https://us.battle.net/oauth/token"
token_data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}
token_response = requests.post(token_url, data=token_data)
token = token_response.json().get('access_token')

if not token:
    print("Failed to get an access token.")
    exit()

headers = {
    "Authorization": f"Bearer {token}"
}

# Item ID for the specific item you want (e.g., 118427)
item_id = "763"

# Construct the item data endpoint URL
item_url = f"https://us.api.blizzard.com/data/wow/item/{item_id}?namespace=static-us&locale=en_US"

# Make a request to the item data endpoint
response = requests.get(item_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    item_data = response.json()

    # Save the item data to a JSON file
    with open('item.json', 'w') as json_file:
        json.dump(item_data, json_file, ensure_ascii=False, indent=4)

    print("Item data has been saved to item.json")
else:
    print(f"Failed to retrieve item data: {response.status_code}")
    print(response.text)  # This will print the error message if any


