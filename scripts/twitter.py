

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