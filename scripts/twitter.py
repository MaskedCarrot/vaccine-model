api_secret_key = 'h8t7UR1kp9gM3mKUjfbKEkrbs404m8E32dZFaFzFT05nikCyBY'
api_key = 'ML0FGGXhhVEuFJBTmUQUAw3Qu'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAA6yLwEAAAAAZLm6jlnzVQhGZ10avjZDKs9uDlg%3DLz8be6Xr4qihErsglUNLArtPt6Vi8Pla8WZMTmZPXoiwB50svZ'
access_token = '1238526226861449216-xN9w63xo9EokhtV5Hus2YdUbpi7w06'
access_secret_token = 'GCYbD2ImidmnEUgRLeXugi1DBQM4x0lOfiN61HOa1a6n0'

import tweepy


auth = tweepy.OAuthHandler(api_key ,  api_secret_key)
auth.set_access_token(access_token, access_secret_token)
api = tweepy.API(auth, wait_on_rate_limit=True)
search_words = 'vaccine'
date_since = "2018-11-16"
# Collect tweets
tweets = tweepy.Cursor(api.search,q=search_words,lang="en",since=date_since).items(5)

for tweet in tweets:
    print(tweet.text)