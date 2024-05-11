# Credentials you get from registering a new application
client_id = '<CLIENT_ID>'
client_secret = '<CLIENT_SECRET>'
config_id = '<CONFIG_ID>'

authorization_base_url = 'https://www.facebook.com/dialog/oauth'
token_url = 'https://graph.facebook.com/oauth/access_token'
redirect_uri = '<Redirect URI>'    

from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
facebook = facebook_compliance_fix(facebook)

authorization_url, state = facebook.authorization_url(authorization_base_url)

print('Please go here and authorize,', authorization_url + f"&config_id={config_id}")

redirect_response = input('Paste the full redirect URL here:')

token = facebook.fetch_token(token_url, client_secret=client_secret,
                 authorization_response=redirect_response)

print(token)