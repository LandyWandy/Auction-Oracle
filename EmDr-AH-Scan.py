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

# Connected realm ID for Emerald Dream
emerald_dream_id = 162

# Construct the auction data endpoint URL
auction_url = f"https://us.api.blizzard.com/data/wow/connected-realm/{emerald_dream_id}/auctions?namespace=dynamic-us&locale=en_US"

# Make a request to the auction data endpoint
response = requests.get(auction_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    auction_data = response.json()

    # Save the auction data to a JSON file
    with open('emerald_dream_auctions.json', 'w') as json_file:
        json.dump(auction_data, json_file, ensure_ascii=False, indent=4)

    print("Auction data has been saved to emerald_dream_auctions.json")
else:
    print(f"Failed to retrieve auction data: {response.status_code}")
    print(response.text)  # This will print the error message if any

# Note: Handle exceptions and potential errors appropriately for production use.
