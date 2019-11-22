
import requests
import json
from statistics import variance
import pandas as pd
import time
import csv
import re

headerIndex = 0
df = pd.read_csv("aggregate_data_set.csv")
csvFile = open('weka_data.csv' ,'a')
fieldnames = [  'user_id', 'num_tweets', 'retweet_ratio', 
                'hashtag_ratio', 'quote_ratio', 'tweet_favorite_ratio',
                'tweet_retweet_ratio', 'mention_ratio', 
                'friend_follower_ratio', 'url_ratio', 'listed_count', 
                'verified', 'geo_enabled', 'protected', 
                'profile_uses_background_image', 'favourites_count',
                'tweet_frequency_variance', 'class']
writer = csv.DictWriter(csvFile, fieldnames)
botOrNotCSV = []
querystring = {"user_id": "", "count": "100"}
headers = [
    {
        'Authorization': "Bearer AAAAAAAAAAAAAAAAAAAAAO99AwEAAAAAyYhojKT%2BfLfFhw4rvWNawjXlgDU%3DqCqeBK5CfwheNK72OABXoNfO5Mgi6UMAgMqtrNt4fcBGqlgHwU"
    },
    {
        'Authorization': "Bearer AAAAAAAAAAAAAAAAAAAAAPB9AwEAAAAAw6tsoRJ6PYu0TXohrlNZFMev1H0%3DFKVNVdLEf3QogWdxGjJ96OEFEFYAu1qUbRowcHIuMZjnU7GjZ4",
    },
]

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
for index, row in df.iterrows():
    hashtagCount = 0
    userMentionsCount= 0
    urlCount = 0
    retweetCount = 0
    quoteCount = 0
    #that the bot's tweets recieve
    numFavorites = 0
    numRetweets = 0
    variance_list = []
    temp = []
    querystring['user_id'] = row['user_id']
    try:
        response = requests.request("GET", url, headers=headers[headerIndex], params=querystring)
    except:
        exit(-1)    
    r = json.loads(response.text)
    if isinstance(r,dict):
        if headerIndex == 1:
            headerIndex = 0
        else:
            headerIndex = 1
        requests.request("GET", url, headers=headers[headerIndex], params=querystring)
        if isinstance(r,dict):
            continue
    tweetCount = len(r)

    if tweetCount <= 3:
        continue
    #had to use indexing instead of an iterator so I could access multiple elements at once
    for i in range(0,tweetCount):
        numFavorites += r[i]['favorite_count']
        numRetweets += r[i]['retweet_count']
        #counts number of each in order to get ratios
        hashtagCount += len(r[i]['entities']['hashtags'])
        userMentionsCount += len(r[i]['entities']['user_mentions'])
        urlCount += len(r[i]['entities']['urls'])
        if re.search('^RT ',r[i]['text']):
            retweetCount+=1
        if r[i]['is_quote_status']:
            quoteCount+=1
        #conversion to epoch time
        if i == 0 or i == tweetCount-1:
            continue
        currentTweet = time.mktime(time.strptime(r[i]['created_at'], "%a %b %d %H:%M:%S +0000 %Y"))
        priorTweet = time.mktime(time.strptime(r[i+1]['created_at'], "%a %b %d %H:%M:%S +0000 %Y"))
        laterTweet = time.mktime(time.strptime(r[i-1]['created_at'], "%a %b %d %H:%M:%S +0000 %Y"))
        #picks the smaller time gap to loop for consistent short bursts of tweets and excludes larger jumps as outliers, should pull bots out better
        if currentTweet-priorTweet <= laterTweet-currentTweet:
            variance_list.append(currentTweet-priorTweet)
        else:
            variance_list.append(laterTweet-currentTweet)

        #class copying into boolean form


  
    writer.writerow(
        {    
        'user_id': row['user_id'],
        'num_tweets': r[0]['user']['statuses_count'],
        'retweet_ratio': retweetCount / tweetCount,
        'hashtag_ratio': hashtagCount / tweetCount,
        'quote_ratio': quoteCount / tweetCount,
        'tweet_favorite_ratio': numFavorites / tweetCount,
        'tweet_retweet_ratio': numRetweets / tweetCount,
        'mention_ratio': userMentionsCount / tweetCount,
        'friend_follower_ratio': r[0]['user']['friends_count'] / (r[0]['user']['followers_count']+1),
        'url_ratio': urlCount / tweetCount,
        'listed_count': r[0]['user']['listed_count'],
        'verified': r[0]['user']['verified'],
        'geo_enabled': r[0]['user']['geo_enabled'],
        'protected': r[0]['user']['protected'],
        'profile_uses_background_image': r[0]['user']['profile_use_background_image'],
        'favourites_count': r[0]['user']['favourites_count'],
        'tweet_frequency_variance': variance(variance_list),
        'class': row['description'] == "bot"
      })