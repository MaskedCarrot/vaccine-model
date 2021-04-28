import csv
import tweepy
import sys

api_secret_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
bearer_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
access_secret_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

args = len(sys.argv)

fieldnames = ['date', 'text']
if(args == 1):
    print("----------test run----------")
    with open('../data/vaccine-tweets.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
    outfile.close()

else:
    auth = tweepy.OAuthHandler(api_key,  api_secret_key)
    auth.set_access_token(access_token, access_secret_token)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    date_since = "2018-11-16"
    tweets = tweepy.Cursor(api.search, q='covaxin -filter:retweets',
                           lang="en", since=date_since).items(1000000)
    json_list = []

    with open('../data/vaccine-tweets.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for tweet in tweets:
            writer.writerow({'date': tweet.created_at,
                            'text': tweet.text.encode('UTF-8')})

    outfile.close()
