from dotenv import load_dotenv
import os
import requests

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

print(token)