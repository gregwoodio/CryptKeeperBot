import requests
from base64 import b64encode
from creds import creds
from TwitterSearch import *
import tweepy
from random import randint
from rhyming_dictionary import rhyme_dict

def get_bearer_token():
	"""get bearer token to authenticate API calls"""
	bearer_token = b64encode(creds['consumer_key'] + ":" + creds['consumer_secret'])
	url = 'https://api.twitter.com/oauth2/token'
	headers = {
		'Authorization': 'Basic ' + bearer_token,
		'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
	}
	data = 'grant_type=client_credentials'
	req = requests.post(url, headers=headers, data=data)
	token = req.json()
	return token

def get_trends(token):
	"""get top 50 trends"""
	url = "https://api.twitter.com/1.1/trends/place.json"
	# id here is WOEID, 1 i world, 4118 is Toronto
	data = {"id":4118}
	headers = {
		'Authorization': 'Bearer ' + token['access_token']
	}
	req = requests.get(url, headers=headers, params=data)

	trends = req.json()[0]["trends"]
	return trends

def search_twitter(*terms):
        """Search Twitter to get tweets from the terms entered"""
	tso = TwitterSearchOrder()
	tso.set_keywords(terms)
	tso.set_language('en')

	ts = TwitterSearch(creds['consumer_key'], creds['consumer_secret'], creds['access_token'], creds['access_token_secret'])
	res = ts.search_tweets(tso)

        return res

def cryptify(tweet):
        """Add a Cryptkeeper pun to the tweet"""
        sender = tweet['user']['screen_name'];
        body = tweet['text']

        new_body = ""
        tweet_words = body.split()
        for word in tweet_words:
            if word in rhyme_dict.keys():
                new_body = body.replace(word, rhyme_dict[word][0].upper())
                break
        
        if len(new_body):
            return "@" + sender + ": " + new_body

        return ""      

def post_tweet(tweet):
       auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
       auth.set_access_token(creds['access_token'], creds['access_token_secret'])
       api = tweepy.API(auth)
       print(tweet)
       api.update_status(tweet)

def main():
	token = get_bearer_token()
        trends = get_trends(token)

	search_terms = trends[randint(0, len(trends) - 1)]["name"]
	#for i in range(3):
	#	search_terms.append(trends[i]["name"])

	print("Search terms: " + str(search_terms))
	res = search_twitter(search_terms)

        terrifying_tweets = []
        for tweet in res['content']['statuses']:
            cryptie = cryptify(tweet)
            if len(cryptie):
                terrifying_tweets.append(cryptie)

        tweet = terrifying_tweets[randint(0, len(terrifying_tweets) - 1)]
        while (len(tweet) > 139):
            tweet = terrifying_tweets[randint(0, len(terrifying_tweets) - 1)]

        post_tweet(tweet)

if __name__ == '__main__':
	main()
