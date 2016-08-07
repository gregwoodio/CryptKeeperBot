import requests
from base64 import b64encode
from creds import creds

# get bearer token to authenticate API calls
bearer_token = b64encode(creds['consumer_key'] + ":" + creds['consumer_secret'])
url = 'https://api.twitter.com/oauth2/token'
headers = {
	'Authorization': 'Basic ' + bearer_token,
	'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
data = 'grant_type=client_credentials'
req = requests.post(url, headers=headers, data=data)
token = req.json()

print("Token type: " + token['token_type'])
print("Access token: " + token['access_token'])

# get top 50 trends
print("\n+---The Top 50 Trends Right Now---+")
url = "https://api.twitter.com/1.1/trends/place.json"
# id here is WOEID, 1 i world, 4118 is Toronto
data = {"id":4118}
headers = {
	'Authorization': 'Bearer ' + token['access_token']
}
req = requests.get(url, headers=headers, params=data)
#print(req.text)
trends = req.json()[0]["trends"]


for trend in trends:
	print(trend["name"])