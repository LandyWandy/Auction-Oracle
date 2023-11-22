import requests
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Your client credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# Function to get a new access token
def get_access_token(client_id, client_secret):
    token_url = "https://us.battle.net/oauth/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, data=token_data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Failed to get access token")
        return None

# Function to fetch item data
def fetch_item_data(item_id, access_token):
    url = f"https://us.api.blizzard.com/data/wow/item/{item_id}?namespace=static-us&access_token={access_token}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for item ID {item_id}: {response.status_code}")
        return None

# Function to read item IDs from file
def read_item_ids(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


# Load item IDs
item_ids = read_item_ids('/Users/temporary/Desktop/Projects/Auction-Oracle-Data/wow_item_ids.txt')

# Constants
BATCH_SIZE = 30000
SLEEP_TIME = 3600  # 1 hour

# Initialize list to store item data
all_item_data = []

# Process in batches
for i in range(0, len(item_ids), BATCH_SIZE):
    # Get a new access token for each batch
    access_token = get_access_token(client_id, client_secret)
    if not access_token:
        break  # Exit if unable to obtain an access token

    batch = item_ids[i:i + BATCH_SIZE]
    for index, item_id in enumerate(batch, start=1):
        print(f"Processing item {i + index} of {len(item_ids)}: ID {item_id}")
        item_data = fetch_item_data(item_id, access_token)
        if item_data:
            all_item_data.append(item_data)
        time.sleep(0.1)  # Sleep to avoid hitting rate limit


    print(f"Completed batch {i//BATCH_SIZE + 1}")
    
    # Sleep after each batch, except the last one
    if i + BATCH_SIZE < len(item_ids):
        print(f"Sleeping for {SLEEP_TIME/3600} hour(s)...")
        time.sleep(SLEEP_TIME)

# Save all item data to JSON file
with open('all_item_data.json', 'w') as file:
    json.dump(all_item_data, file, indent=4)

print("All data has been fetched and saved.")
