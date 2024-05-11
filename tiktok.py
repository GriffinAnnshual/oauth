import hashlib
import base64
import os
from requests_oauthlib import OAuth2Session

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client_key = '<CLIENT_KEY>'  
client_secret = '<CLIENT_SECRET>'

scope = ["user.info.basic"]  
redirect_uri = 'http://localhost:3000/connect_channels' 

authorization_base_url = 'https://www.tiktok.com/v2/auth/authorize/'
token_url = 'https://www.tiktok.com/v2/auth/access_token/' 

code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
code_verifier = code_verifier.rstrip('=')

code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8')
code_challenge = code_challenge.rstrip('=')

tiktok = OAuth2Session(client_key, redirect_uri=redirect_uri, scope=scope)

authorization_url, state = tiktok.authorization_url(authorization_base_url, code_challenge_method='S256', code_challenge=code_challenge)
print(f"Please go here and authorize: {authorization_url}")


# def fetch_access_token(authorization_code):
#     data = {
#         'client_key': client_key,
#         'client_secret': client_secret,
#         'code': authorization_code,
#         'grant_type': 'authorization_code',
#         'redirect_uri': redirect_uri
#     }
#     response = requests.post(token_url, data=data)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return response.json()

# def refresh_access_token(refresh_token):
#     data = {
#         'client_key': client_key,
#         'client_secret': client_secret,
#         'grant_type': 'refresh_token',
#         'refresh_token': refresh_token
#     }
#     response = requests.post(token_url, data=data)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return response.json()