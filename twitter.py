from requests_oauthlib import OAuth1Session

consumer_key = '<CONSUMER_KEY>'
consumer_secret = '<CONSUMER_SECRET>'
resource_owner_key = ''
resource_owner_secret = ''
callback = "http://localhost:3000/connect_channels"

def twitter_get_oauth_request_token():
    global resource_owner_key
    global resource_owner_secret
    request_token = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret, callback_uri=callback)
    url = 'https://api.twitter.com/oauth/request_token'
    data = request_token.get(url)
    print(data.text)
    data_token = str.split(data.text, '&')
    ro_key = str.split(data_token[0], '=')
    ro_secret = str.split(data_token[1], '=')
    resource_owner_key = ro_key[1]
    resource_owner_secret = ro_secret[1]
    resource = [resource_owner_key, resource_owner_secret]
    return resource


def twitter_get_oauth_token(verifier, ro_key, ro_secret):
    oauth_token = OAuth1Session(client_key=consumer_key,
                                client_secret=consumer_secret,
                                resource_owner_key=ro_key,
                                resource_owner_secret=ro_secret)
    url = 'https://api.twitter.com/oauth/access_token'
    data = {"oauth_verifier": verifier}
    print(ro_key)
    print(ro_secret)
    access_token_data = oauth_token.post(url, data=data)
    print(access_token_data.text)
    access_token_list = str.split(access_token_data.text, '&')
    return access_token_list


def twitter_get_access_token(access_token_list):
    access_token_key = str.split(access_token_list[0], '=')
    access_token_secret = str.split(access_token_list[1], '=')
    access_token_name = str.split(access_token_list[3], '=')
    access_token_id = str.split(access_token_list[2], '=')
    key = access_token_key[1]
    secret = access_token_secret[1]
    name = access_token_name[1]
    id = access_token_id[1]
    oauth_user = OAuth1Session(client_key=consumer_key,
                               client_secret=consumer_secret,
                               resource_owner_key=key,
                               resource_owner_secret=secret)
    url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    params = {"include_email": 'true'}
    user_data = oauth_user.get(url_user, params=params)
    print(user_data.json())
    return user_data.json()


list = twitter_get_oauth_request_token()
req_key, req_secret = list[0], list[1]
url = "https://api.twitter.com/oauth/authenticate?oauth_token=" + req_key
print(url)


oauth_verifier = input("Enter the oauth verifier: ")

list = twitter_get_oauth_token(oauth_verifier,req_key,req_secret)
print(twitter_get_access_token(list))