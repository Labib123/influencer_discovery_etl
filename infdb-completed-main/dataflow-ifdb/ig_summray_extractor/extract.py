import time

from instaloader import Instaloader, Profile
import datetime
import json

MAX_DAYS = 45

LIKES_WEIGHT = 1
COMMENTS_WEIGHT = 1
NUM_FOLLOWERS_WEIGHT = 1
NUM_POSTS_WEIGHT = 1

loader = Instaloader()

USER = "infdbdev1@gmail.com"
PASSWORD = "Striveforperfectionineverythingyoudo"
#
#
loader.login(USER, PASSWORD)

current_date = datetime.datetime.now()


# print(profile.biography)
#
# print(profile.profile_pic_url)
#


def get_profiles():
    profiles = []

    with open('../s3_local/inf_data.json', 'r') as f:
        data = json.load(f)

        for inf in data['instagram']['data']:
            profiles.append(inf[0])

    return profiles


def get_summary(USERNAME):
    profile = Profile.from_username(loader.context, USERNAME)

    user = {'id': profile.username, 'followers': profile.followers}

    posts = []
    total_num_likes = 0
    total_num_comments = 0
    total_num_posts = 0
    total_likes = set()

    for post in profile.get_posts():
        delta = current_date - post.date

        dt_time = post.date.date()

        int_date = 10000 * dt_time.year + 100 * dt_time.month + dt_time.day
        total_likes = total_likes | set(post.get_likes())

        posts.append({"username": post.owner_username, "url": post.url, "likes": post.likes, "comments": post.comments,
                      "dates": int_date, "captions": post.caption, "followers": profile.followers})

        if delta.days > MAX_DAYS:
            break
        if post.likes is not None:
            total_num_likes += post.likes
        if post.comments is not None:
            total_num_comments += post.comments
        total_num_posts += 1

    print("total likes no: {0}".format(total_likes))

    user['num_recent_posts'] = total_num_posts

    user['total_likes'] = total_likes

    user['total_num_comments'] = total_num_comments

    user['latest_posts'] = posts

    return user


def extract_single_profile(profile):

    print("Started Extracting data for:{0} ".format(profile))

    summary = get_summary(profile)

    print(summary)

    with open('summary_data_{0}_{1}.json'.format(profile, current_date), 'w') as sf:
        json.dump(summary, sf, default=int)


def test_extract(username):
    profile = Profile.from_username(loader.context, username)

    # should be while less than one year
    # and then extract the post.likes

    for post in profile.get_posts():
        delta = current_date - post.date

        if delta.days > MAX_DAYS:
            break


def extract():
    profiles_summary = []

    profiles = get_profiles()
    print("Loaded {} profiles".format(len(profiles)))

    for idx, profile in enumerate(profiles):
        summary = get_summary(profile)
        profiles_summary.append(summary)
        print(summary)
        time.sleep(5)

    with open('summary_data_{0}.json'.format(current_date), 'w') as sf:
        json.dump(profiles_summary, sf)


def extract_ghost_followers(profile):
    profile = Profile.from_username(loader.context, profile)

    likes = set()
    print("Fetching likes of all posts of profile {}.".format(profile.username))

    for post in profile.get_posts():
        print(post)
        likes = likes | set(post.get_likes())

    # for post in profile.get_posts():
    #     print(post)
    #     likes = likes | set(post.get_likes())
    #
    # print("Fetching followers of profile {}.".format(profile.username))
    # followers = set(profile.get_followers())
    #
    # ghosts = followers - likes
    #
    # print("Storing ghosts into file.")
    # with open("inactive-users.txt", 'w') as f:
    #     for ghost in ghosts:
    #         print(ghost.username, file=f)


# extract()
# extract_ghost_followers("afshaa17")


extract_single_profile("afshaa17")
# test_extract("afshaa17")
