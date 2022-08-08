import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None)
import numpy as np

import datetime as dt

import seaborn as sns
import matplotlib.pyplot as plt

import warnings

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.model_selection import train_test_split, GridSearchCV

import joblib

warnings.filterwarnings('ignore')

df = pd.read_json("./summary_data_afshaa17_2022-04-17 07:33:35.659370.json")

# data cleansing


# convert epoch time --> datetime
# The format is year-month-day-hour
df['dates'] = df['dates'].apply(lambda x: str(dt.datetime.strptime(str(x), '%Y%M%d').date()))

# remove unused characters in feature captions
df['captions'] = df['captions'].replace(r'[\n]', '', regex=True)
# fill missing value in features captions
df['captions'] = df['captions'].fillna('no captions')

# separte for future use
df['year'] = df['dates'].apply(lambda x: x[:4])
df['month'] = df['dates'].apply(lambda x: x[5:7])
df['day'] = df['dates'].apply(lambda x: x[8:10])
df['hour'] = df['dates'].apply(lambda x: x[11:])

# create year_month features
df['year_month'] = df['year'] + df['month']

# Feature Selection
# I choose variables with the value of correlation coefficient r < -0.2 and r > 0.3
# it is very subjective matter
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr())

base_table = df.groupby(['username', 'year_month']).agg({
    'url': 'count'
}).reset_index().rename(columns={
    'url': 'n_post'
})

# Create our target Variable
base_table['y_month_01'] = base_table.groupby(['username'])['avg_total_engagement'].shift(-1).fillna(0)

# create features lag of n_post (last 3 month)
# number of n_post 1 months ago
base_table['n_post_01'] = base_table.groupby(['username'])['n_post'].shift(1).fillna(0)

# number of n_post 2 months ago
base_table['n_post_02'] = base_table.groupby(['username'])['n_post'].shift(2).fillna(0)

# number of n_post 3 months ago
base_table['n_post_03'] = base_table.groupby(['username'])['n_post'].shift(3).fillna(0)

df_type_post = df.groupby(['username', 'year_month'])['type_posts'].value_counts().unstack(2).reset_index().fillna(0)

base_table['n_img_post'] = df_type_post['GraphImage']
base_table['n_vid_post'] = df_type_post['GraphVideo']
base_table['n_sidecar_post'] = df_type_post['GraphSidecar']

# create features sum, avg and stdev of likes
base_table['sum_likes'] = df.groupby(['username', 'year_month'])['likes'].sum().reset_index()['likes']
base_table['avg_likes'] = df.groupby(['username', 'year_month'])['likes'].mean().reset_index()['likes']
base_table['std_likes'] = df.groupby(['username', 'year_month'])['likes'].std().reset_index()['likes'].fillna(0)

# create features lag of sum_likes and mean_likes (last 3 month)
base_table['avg_likes_01'] = base_table.groupby(['username'])['avg_likes'].shift(1).fillna(0)
base_table['avg_likes_02'] = base_table.groupby(['username'])['avg_likes'].shift(2).fillna(0)
base_table['avg_likes_03'] = base_table.groupby(['username'])['avg_likes'].shift(3).fillna(0)

base_table['sum_likes_01'] = base_table.groupby(['username'])['sum_likes'].shift(1).fillna(0)
base_table['sum_likes_02'] = base_table.groupby(['username'])['sum_likes'].shift(2).fillna(0)
base_table['sum_likes_03'] = base_table.groupby(['username'])['sum_likes'].shift(3).fillna(0)

# create features sum, avg and stdev of comments
base_table['sum_comments'] = df.groupby(['username', 'year_month'])['comment_counts'].sum().reset_index()[
    'comment_counts']
base_table['avg_comments'] = df.groupby(['username', 'year_month'])['comment_counts'].mean().reset_index()[
    'comment_counts']
base_table['std_comments'] = df.groupby(['username', 'year_month'])['comment_counts'].std().reset_index()[
    'comment_counts'].fillna(0)

# create features lag of sum_comments and mean_comments (last 3 month)
base_table['avg_comments_01'] = base_table.groupby(['username'])['avg_comments'].shift(1).fillna(0)
base_table['avg_comments_02'] = base_table.groupby(['username'])['avg_comments'].shift(2).fillna(0)
base_table['avg_comments_03'] = base_table.groupby(['username'])['avg_comments'].shift(3).fillna(0)

base_table['sum_comments_01'] = base_table.groupby(['username'])['sum_comments'].shift(1).fillna(0)
base_table['sum_comments_02'] = base_table.groupby(['username'])['sum_comments'].shift(2).fillna(0)
base_table['sum_comments_03'] = base_table.groupby(['username'])['sum_comments'].shift(3).fillna(0)

# create features sum, avg and stdev of captions_wo_punct
base_table['sum_capt_wo_punct'] = df.groupby(['username', 'year_month'])['len_capt_wo_punct'].sum().reset_index()[
    'len_capt_wo_punct']
base_table['avg_capt_wo_punct'] = df.groupby(['username', 'year_month'])['len_capt_wo_punct'].mean().reset_index()[
    'len_capt_wo_punct']
base_table['std_capt_wo_punct'] = df.groupby(['username', 'year_month'])['len_capt_wo_punct'].std().reset_index()[
    'len_capt_wo_punct'].fillna(0)

# create features sum, avg and stdev of captions_w_punct
base_table['sum_capt_w_punct'] = df.groupby(['username', 'year_month'])['len_capt_punct'].sum().reset_index()[
    'len_capt_punct']
base_table['avg_capt_w_punct'] = df.groupby(['username', 'year_month'])['len_capt_punct'].mean().reset_index()[
    'len_capt_punct']
base_table['std_capt_w_punct'] = df.groupby(['username', 'year_month'])['len_capt_punct'].std().reset_index()[
    'len_capt_punct'].fillna(0)

# create features sum, avg and stdev of n_words
base_table['sum_n_words'] = df.groupby(['username', 'year_month'])['n_words'].sum().reset_index()['n_words']
base_table['avg_n_words'] = df.groupby(['username', 'year_month'])['n_words'].mean().reset_index()['n_words']
base_table['std_n_words'] = df.groupby(['username', 'year_month'])['n_words'].std().reset_index()['n_words'].fillna(0)

# create features sum, avg and stdev of avg_char_words
base_table['sum_avg_char_words'] = df.groupby(['username', 'year_month'])['avg_char_words'].sum().reset_index()[
    'avg_char_words']
base_table['avg_avg_char_words'] = df.groupby(['username', 'year_month'])['avg_char_words'].mean().reset_index()[
    'avg_char_words']
base_table['std_avg_char_words'] = df.groupby(['username', 'year_month'])['avg_char_words'].std().reset_index()[
    'avg_char_words'].fillna(0)

# create features lag of captions (last 3 month)
base_table['sum_capt_wo_punct_01'] = base_table.groupby(['username'])['sum_capt_wo_punct'].shift(1).fillna(0)
base_table['sum_capt_wo_punct_02'] = base_table.groupby(['username'])['sum_capt_wo_punct'].shift(2).fillna(0)
base_table['sum_capt_wo_punct_03'] = base_table.groupby(['username'])['sum_capt_wo_punct'].shift(3).fillna(0)

base_table['sum_capt_w_punct_01'] = base_table.groupby(['username'])['sum_capt_w_punct'].shift(1).fillna(0)
base_table['sum_capt_w_punct_02'] = base_table.groupby(['username'])['sum_capt_w_punct'].shift(2).fillna(0)
base_table['sum_capt_w_punct_03'] = base_table.groupby(['username'])['sum_capt_w_punct'].shift(3).fillna(0)

base_table['sum_n_words_01'] = base_table.groupby(['username'])['sum_n_words'].shift(1).fillna(0)
base_table['sum_n_words_02'] = base_table.groupby(['username'])['sum_n_words'].shift(2).fillna(0)
base_table['sum_n_words_03'] = base_table.groupby(['username'])['sum_n_words'].shift(3).fillna(0)

base_table['sum_avg_char_words_01'] = base_table.groupby(['username'])['sum_avg_char_words'].shift(1).fillna(0)
base_table['sum_avg_char_words_02'] = base_table.groupby(['username'])['sum_avg_char_words'].shift(2).fillna(0)
base_table['sum_avg_char_words_03'] = base_table.groupby(['username'])['sum_avg_char_words'].shift(3).fillna(0)

base_table['sum_n_numeric'] = df.groupby(['username', 'year_month'])['n_numeric'].sum().reset_index()['n_numeric']

# create features sum and avg engagement
base_table['sum_likes_engagement'] = df.groupby(['username', 'year_month'])['likes_engagement'].sum().reset_index()[
    'likes_engagement']
base_table['sum_comments_engagement'] = \
df.groupby(['username', 'year_month'])['comments_engagement'].sum().reset_index()['comments_engagement']
base_table['sum_total_engagement'] = df.groupby(['username', 'year_month'])['total_engagement'].sum().reset_index()[
    'total_engagement']

base_table['avg_likes_engagement'] = df.groupby(['username', 'year_month'])['likes_engagement'].mean().reset_index()[
    'likes_engagement']
base_table['avg_comments_engagement'] = \
df.groupby(['username', 'year_month'])['comments_engagement'].mean().reset_index()['comments_engagement']
base_table['avg_total_engagement'] = df.groupby(['username', 'year_month'])['total_engagement'].mean().reset_index()[
    'total_engagement']

# create features lag of engagement (last 3 month)
base_table['avg_total_engagement_01'] = base_table.groupby(['username'])['avg_total_engagement'].shift(1).fillna(0)
base_table['avg_total_engagement_02'] = base_table.groupby(['username'])['avg_total_engagement'].shift(2).fillna(0)
base_table['avg_total_engagement_03'] = base_table.groupby(['username'])['avg_total_engagement'].shift(3).fillna(0)

# because the count of post before 2018 is small, we only filter post that >= 2018
# and our objective is to predict avg engagment rate in July 2020, so we must exclude July 2020 too.
df_2 = df[df['year'] >= '2018'].reset_index(drop=True)
df_3 = df_2[df_2['year_month'] != '202007'].reset_index(drop=True)

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

print(df_3.head())

df_3.to_csv("processed.csv", index=False)

df = pd.read_csv(r'./processed.csv')

# i choose variables with the value of correlation coefficient r < -0.2 and r > 0.3
# it is very subjective matter
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr())

feature = ['username', 'year_month', 'n_post', 'n_post_01', 'n_img_post', 'avg_likes', 'avg_likes_01', 'avg_likes_02',
           'avg_likes_03', 'sum_capt_wo_punct', 'sum_n_words', 'sum_avg_char_words', 'sum_likes_engagement',
           'sum_total_engagement', 'avg_likes_engagement', 'avg_total_engagement', 'avg_total_engagement_01',
           'avg_total_engagement_02', 'avg_total_engagement_03', 'y_month_01']

# remove outliers
df = df[df['y_month_01'] <= 20].reset_index(drop=True)

sns.distplot(df['y_month_01'])

df_w_feat = df[feature]
df_wo_feat = df.copy(deep=True)

# splitting the data for prediction and for training
df_prediction_1 = df_wo_feat[df_wo_feat['year_month'] == 202006].reset_index(drop=True)
df_training_1 = df_wo_feat[df_wo_feat['year_month'] != 202006].reset_index(drop=True)

