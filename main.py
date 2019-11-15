import requests
import json

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
querystring = {"user_id": "390617262"}
headers = {
    'Authorization': "Bearer AAAAAAAAAAAAAAAAAAAAAPB9AwEAAAAAw6tsoRJ6PYu0TXohrlNZFMev1H0%3DFKVNVdLEf3QogWdxGjJ96OEFEFYAu1qUbRowcHIuMZjnU7GjZ4",
}

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

tweets = []

r = response.text

for r in json.loads(response.text):
    id = r['id']
    retweet_created_at = r['created_at']
    # retweeted_tweet_created_at = r['retweeted_status']['created_at']

    print(id, retweet_created_at)
