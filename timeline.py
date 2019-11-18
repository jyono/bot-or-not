# ugly/hacky example of requesting from twitter api

import requests
import json
import pandas as pd

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
headers = {
    'Authorization': "Bearer AAAAAAAAAAAAAAAAAAAAAPB9AwEAAAAAw6tsoRJ6PYu0TXohrlNZFMev1H0%3DFKVNVdLEf3QogWdxGjJ96OEFEFYAu1qUbRowcHIuMZjnU7GjZ4",
}

df = pd.read_csv('aggregate_data_set', sep=",", header=None)
df.columns = ['user_id', 'description']
# querystring = {"user_id": "390617262"}
# response = requests.request("GET", url, headers=headers, params=querystring)
# r = response.text

for index in df.index:
    user_id = df['user_id'][index]
    querystring = {"user_id": user_id}
    response = requests.request("GET", url, headers=headers, params=querystring)
    # print(df['user_id'][index])
    # print(response.json())

    print('***************************************\n\n\n\n\n**********************************')
    for r in json.loads(response.text):
        if type(r) == dict:
            print(r['id'])
            if 'retweeted_status' in r:
                print('meow')
            else:
                print('woof')
        if type(r) == str:
            print('-----------------------------------------')
            print('error')
            print('-----------------------------------------')
