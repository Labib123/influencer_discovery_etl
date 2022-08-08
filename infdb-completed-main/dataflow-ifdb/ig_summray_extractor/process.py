# Instagram data processing + feature engineering
# Inspired by this repo: https://github.com/adiptamartulandi/Project-Instagram-Influencers-Prediction

import pandas as pd
import warnings
import datetime as dt

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
current_date = dt.date.today()

# Load Data
df = pd.read_json(r'summary_data_afshaa17_2022-04-17 07:33:35.659370.json')

print(df.shape)

# convert epoch time --> datetime
# The format is year-month-day-hour
df['dates'] = df['dates'].apply(lambda x: str(dt.datetime.strptime(str(x), '%Y%M%d').date()))

# remove unused characters in feature captions
df['captions'] = df['captions'].replace(r'[\n]', '', regex=True)
# fill missing value in features captions
df['captions'] = df['captions'].fillna('no captions')

# separate for future use
df['year'] = df['dates'].apply(lambda x: x[:4])
df['month'] = df['dates'].apply(lambda x: x[5:7])
df['day'] = df['dates'].apply(lambda x: x[8:10])
df['hour'] = df['dates'].apply(lambda x: x[11:])

# create year_month features
df['year_month'] = df['year'] + df['month']

# print(df['dates'].min())
# print(df['dates'].max())

# because the count of post before 2018 is small, we only filter post that >= 2018
# and our objective is to predict avg engagment rate in July 2020, so we must exclude July 2020 too.
df_2 = df[df['year'] >= '2018'].reset_index(drop=True)
df_3 = df_2[df_2['year_month'] != '202007'].reset_index(drop=True)

# exclude ghost followers
df_3['followers'] = df_3['followers'] - df_3['ghost_followers']

df_3['likes_engagement'] = df_3['likes'] / df_3['followers'] * 100
df_3['comments_engagement'] = df_3['comments'] / df_3['followers'] * 100

df_3['total_engagement'] = df_3['likes_engagement'] + df_3['comments_engagement']
# make lower case
df_3['captions'] = df_3['captions'].str.lower()

# delete whitespace
df_3['captions'] = df_3['captions'].str.strip()

# feature length of captions
df_3['len_capt'] = df_3['captions'].apply(lambda x: len(x))

# create feature length of captions without punctuation
df_3['len_capt_wo_punct'] = df_3['captions'].str.replace(r'[^\w\s]', '', regex=True).apply(lambda x: len(x))

# feature length of punctuation only
df_3['len_capt_punct'] = df_3['captions'].str.replace(r'[\w\s]', '', regex=True).apply(lambda x: len(x))

# feature number of words in each captions
df_3['n_words'] = df_3['captions'].apply(lambda x: len(str(x).split(" ")))

# average char per words
df_3['avg_char_words'] = df_3['n_words'] / df_3['len_capt']

# number of numeric char in captions
df_3['n_numeric'] = df_3['captions'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))

print(df_3.shape)

df_3.to_csv('summary_data_processed_{0}.csv'.format(current_date), index=False)


# ghost_followers = profile.followers - total_likes
# posts.append({"ghost_followers": ghost_followers})
#
# if profile.followers > 0 and total_num_posts > 0:
#     engagement = float((LIKES_WEIGHT * total_num_likes) + (COMMENTS_WEIGHT * total_num_comments)) / (
#             (NUM_FOLLOWERS_WEIGHT * profile.followers) * (NUM_POSTS_WEIGHT * total_num_posts))

# post_freq = 0.0
# if total_num_posts > 0:
#     post_freq = float(MAX_DAYS) / total_num_posts
# user['post_frequency'] = post_freq
# user['engagement'] = engagement * 100
