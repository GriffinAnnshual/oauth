import os
from requests_oauthlib import OAuth2Session
import requests

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client_id = '<CLIENT_ID>'
client_secret = '<CLIENT_SECERT>'


scope = ["r_ads_reporting","r_ads","r_organization_admin"]

authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'

linkedin = OAuth2Session(client_id, redirect_uri='http://localhost:3000/connect_channels', scope=scope)

authorization_url, state = linkedin.authorization_url(authorization_base_url)
print(f"Please go here and authorize: {authorization_url}")

redirect_response = input('Paste the full redirect URL here:')

token = linkedin.fetch_token(token_url, client_secret=client_secret,
                             include_client_id=True,
                             authorization_response=redirect_response)

print(token['access_token'])

access_token = token['access_token']

headers = {
    'Authorization': f'Bearer {access_token}',
    'X-Restli-Protocol-Version': '2.0.0'
}

url = 'https://api.linkedin.com/v2/adCreativesV2'

response = requests.get(url, headers=headers)

data = response.json()

print(data)