import pandas as pd

# normalize the data and aggregate into one file

#  output-onlinetsvtools.txt
#  ex. 1234567890,human
df = pd.read_csv('output-onlinetsvtools.txt', sep=",", header=None)
df.columns = ['user_id', 'description']

# gilani-2017.tsv
# 1234567890    human
df2 = pd.read_csv('gilani-2017.tsv', sep='\t', header=None)
df2.columns = ['user_id', 'description']

# varol-2017.csv
# 1 means that it is a bot and 0 is a human
# 3098421349	1
df3 = pd.read_csv('varol-2017.csv', sep=',', header=None)
df3.columns = ['user_id', 'description']

# use the is_bot to write to the description column then delete isBot column
df3['description'] = df3['description'].replace(1, 'bot').replace(0, 'human')

df_merge = df.append(df2).append(df3)
df_merge.to_csv('aggregate_data_set', index=False)