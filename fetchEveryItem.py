import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

# Blizzard API credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Get an access token
def get_access_token():
    token_url = "https://us.battle.net/oauth/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    token_response = requests.post(token_url, data=token_data)
    return token_response.json().get('access_token')

token = get_access_token()

if not token:
    print("Failed to get an access token.")
    exit()

# Function to fetch data from API
def fetch_data(starting_item, access_token):
    url = f"https://us.api.blizzard.com/data/wow/search/item?namespace=static-us&orderby=id&_pageSize=1000&id=[{starting_item},]&_page=1&access_token={access_token}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve data: {e}")
        return None

# Initialize variables
all_items = []
starting_item = 1
has_more_data = True

# Fetch and store data
while has_more_data:
    data = fetch_data(starting_item, token)
    if data and data.get('results'):
        all_items.extend(data['results'])
        starting_item = data['results'][-1]['data']['id'] + 1
        print(f"Fetched items up to ID {starting_item - 1}")
    else:
        has_more_data = False
    time.sleep(1)  # Delay to prevent hitting rate limits

# Save to JSON file
with open('wow_items.json', 'w') as file:
    json.dump(all_items, file, indent=4)

print("Data saved to wow_items.json")
