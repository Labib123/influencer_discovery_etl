import json
import time
import datetime
from instaloader import Instaloader, Profile

MAX_DAYS = 30

LIKES_WEIGHT = 1
COMMENTS_WEIGHT = 1
NUM_FOLLOWERS_WEIGHT = 1
NUM_POSTS_WEIGHT = 1
CURRENT_DATE = datetime.datetime.now()

loader = Instaloader()


def login():
    USER = "infdbdev2@gmail.com"
    PASSWORD = "Striveforperfectionineverythingyoudo"

    loader.login(USER, PASSWORD)

    print("Logged in using {} account".format(USER.split("@")[0]))

# with open('ig_summary_20220207.json', 'r') as f:
#     data = json.load(f)
#
#     print(data[-1]['id'])


def get_summary(USERNAME):
    profile = Profile.from_username(loader.context, USERNAME)

    user = {'id': profile.username}

    posts = []

    print('Engagement Get Summary: {}'.format(profile.username))

    total_num_likes = 0
    total_num_comments = 0
    total_num_posts = 0

    for idx, post in enumerate(profile.get_posts()):
        delta = CURRENT_DATE - post.date

        if idx > 5:
            posts.append({"url": post.url, "likes": post.likes, "comments": post.comments})

        if delta.days > MAX_DAYS:
            break
        if post.likes is not None:
            total_num_likes += post.likes
        if post.comments is not None:
            total_num_comments += post.comments
        total_num_posts += 1

    engagement = 0
    if profile.followers > 0 and total_num_posts > 0:
        engagement = float((LIKES_WEIGHT * total_num_likes) + (COMMENTS_WEIGHT * total_num_comments)) / (
                (NUM_FOLLOWERS_WEIGHT * profile.followers) * (NUM_POSTS_WEIGHT * total_num_posts))
    user['engagement'] = engagement * 100
    print('  Engagement: {}'.format(user['engagement']))
    user['num_recent_posts'] = total_num_posts
    print('  Number of Recent Posts: {}'.format(user['num_recent_posts']))
    post_freq = 0.0
    if total_num_posts > 0:
        post_freq = float(MAX_DAYS) / total_num_posts
    user['post_frequency'] = post_freq

    user['latest_posts'] = posts

    return user


def get_profiles(last_client):
    with open('file.json', 'r') as f:
        data = json.load(f)

        profiles = data['instagram']['data']

        last_client_idx = 0

        for idx, profile in enumerate(profiles):
            if profile[0] == last_client:
                last_client_idx = idx + 1

    return profiles[last_client_idx:]


def extract():
    login()

    with open('../s3_local/raw/instagram/ig_summary_20220207.json', 'r') as f:
        profiles_ids = json.load(f)
        last_profile = profiles_ids[-1]['id']
        profiles = get_profiles(last_profile)

    print("Loaded {} profiles".format(len(profiles)))

    for idx, profile in enumerate(profiles):
        print("Loading {} profile summary".format(profile[0]))
        summary = get_summary(profile[0])
        print("successfully updated {} profile summary".format(summary['id']))
        time.sleep(5)
        print("Saving {} profile summary to S3".format(summary['id']))
        with open('ig_summary_20220207.json'.format(CURRENT_DATE), 'a') as sf:
            json.dump(summary, sf)
        print("successfully saved {} profile summary to S3 ".format(summary['id']))


