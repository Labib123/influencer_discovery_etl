import json
import time

import psycopg2

platform_map = {"instagram": "ig_id", "tiktok": "tiktok_id", "youtube": "youtube_id", "twitter": "twitter_id",
                "twitch": "twitch_id"}

conn = psycopg2.connect(
    host="localhost",
    database="infdb_dev",
    user="infdb_admin",
    password="admmin@133")


def connect():
    try:
        print('Connecting to the PostgreSQL database...')
        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()

        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_top_100():
    cur = conn.cursor()

    with open('../../dataflow-ifdb/s3_local/inf_data.json', 'r') as f:
        data = json.load(f)

        for platform in data:
            accounts_no = 0

            if platform == 'instagram':

                sql = "INSERT INTO public.{0} (id, followers, " \
                      "following, rank, name) VALUES (%s, %s,%s, %s," \
                      "%s) ON CONFLICT ON CONSTRAINT {0}_pk DO UPDATE set " \
                      "followers = EXCLUDED.followers  " \
                      "  returning id; ".format(platform)

                for influencer in data[platform]['data']:

                    if_id = influencer[0]

                    name = influencer[2]
                    followers = int(influencer[3].replace(',', ''))
                    following = influencer[4]
                    posts = int(influencer[5].replace(',', ''))

                    rank = '1'
                    # (platform, id, followers, following, rank, platform)

                    val = (if_id, followers, following, rank, name)

                    cur.execute(sql, val)

                    if cur.fetchone is not None:
                        accounts_no += 1

            if platform == 'twitch':

                sql = "INSERT INTO public.twitch (id, followers, " \
                      " views) VALUES (%s, %s, %s) ON CONFLICT ON CONSTRAINT twitch_pk DO UPDATE set " \
                      "views " \
                      " = EXCLUDED.views returning id; "

                for influencer in data[platform]['data']:
                    if_id = influencer[0]
                    rank = influencer[1]

                    followers = int(influencer[3].replace(',', ''))

                    views = int(influencer[4].replace(',', ''))

                    # (platform, id, followers, following, tweets , platform)

                    val = (if_id, followers, views)

                    cur.execute(sql, val)

                    if cur.fetchone is not None:
                        accounts_no += 1

            if platform == 'twitter':

                sql = "INSERT INTO public.twitter (id, followers, " \
                      "following, tweets) VALUES (%s, %s,%s, %s) ON CONFLICT ON CONSTRAINT twitter_pk DO UPDATE set " \
                      "followers " \
                      " = EXCLUDED.followers returning id; "

                for influencer in data[platform]['data']:
                    if_id = influencer[0]
                    name = influencer[2]
                    followers = int(influencer[3].replace(',', ''))
                    following = influencer[4]
                    tweets = int(influencer[5].replace(',', ''))

                    rank = '1'
                    # (platform, id, followers, following, tweets , platform)

                    val = (if_id, followers, following, tweets)

                    cur.execute(sql, val)

                    if cur.fetchone is not None:
                        accounts_no += 1

            if platform == 'youtube':

                sql = "INSERT INTO public.youtube (id,  " \
                      "subscribers, views, videos) VALUES (%s,%s, %s, %s) ON CONFLICT ON CONSTRAINT youtube_pk DO " \
                      "UPDATE set " \
                      "subscribers " \
                      " = EXCLUDED.subscribers returning id; "

                for influencer in data[platform]['data']:
                    if_id = influencer[0]
                    rank = influencer[1]
                    name = influencer[2]
                    subscribers = int(influencer[3].replace(',', ''))
                    views = int(influencer[4].replace(',', ''))
                    videos = int(influencer[5].replace(',', ''))

                    val = (if_id, subscribers, views, videos)

                    cur.execute(sql, val)

                    if cur.fetchone is not None:
                        accounts_no += 1

            conn.commit()

            print("{0} {1} Profiles has been successfully updated ".format(accounts_no, platform))


def insert_summary():
    print("Loading summary data")

    cur = conn.cursor()

    with open('s3_local/raw/instagram/ig_summary_20220207.json', 'r') as sf:
        data = json.load(sf)
        # print(data)

        for inf in data:
            if_id = inf['id']

            engagement = inf['engagement']

            num_recent_posts = inf['num_recent_posts']

            bio = inf['bio']

            profile_pic_url = inf['profile_pic_url']

            sql = "INSERT INTO public.instagram (id, engagement, " \
                  "num_recent_posts, bio, profile_pic_url) VALUES (%s, %s,%s, %s," \
                  "%s) ON CONFLICT ON CONSTRAINT instagram_pk DO UPDATE set " \
                  "engagement = EXCLUDED.engagement,  " \
                  "num_recent_posts = EXCLUDED.num_recent_posts , " \
                  "bio = EXCLUDED.bio , " \
                  "profile_pic_url = EXCLUDED.profile_pic_url  " \
                  "  returning id; "

            val = (if_id, engagement, num_recent_posts, bio, profile_pic_url)

            cur.execute(sql, val)

        conn.commit()


def insert_ig_profiles():
    cur = conn.cursor()

    sql = "select * from public.instagram"

    cur.execute(sql)

    result = cur.fetchall()

    profiles = []

    for profile in result:
        profiles.append(profile[1])

    with open('s3_local/config/ig_profiles.json', 'w') as f:
        json.dump(profiles, f)


if __name__ == '__main__':
    # connect()
    # insert_top_100()
    # insert_summary()
    insert_ig_profiles()


def insert_metadata():
    print("Loading summary data")

    cur = conn.cursor()

    with open('s3_local/raw/instagram/ig_meta_20220206.json', 'r') as sf:
        data = json.load(sf)['data']

        print("Loaded {} profiles".format(len(data)))

        for inf in data:
            if_id = inf['id']

            following = inf['following']

            followers = inf['followers']

            business_category_name = inf['business_category_name']

            external_url = inf['external_url']

            is_verified = inf['is_verified']

            bio = inf['bio']

            profile_pic_url = inf['profile_pic_url']

            sql = "INSERT INTO public.instagram (id, following, " \
                  "followers, bio, profile_pic_url, business_category_name, external_url, is_verified) VALUES (%s, " \
                  "%s,%s, %s," \
                  "%s, %s, %s, %s) ON CONFLICT ON CONSTRAINT instagram_pk DO UPDATE set " \
                  "following = EXCLUDED.following,  " \
                  "followers = EXCLUDED.followers , " \
                  "bio = EXCLUDED.bio , " \
                  "profile_pic_url = EXCLUDED.profile_pic_url,  " \
                  "business_category_name = EXCLUDED.business_category_name , " \
                  "external_url = EXCLUDED.external_url , " \
                  "is_verified = EXCLUDED.is_verified  " \
                  "  returning id; "

            val = (if_id, following, followers, bio, profile_pic_url, business_category_name, external_url, is_verified)

            cur.execute(sql, val)

        conn.commit()
        print("Inserted {} profiles".format(len(data)))


# insert_metadata()


def test():
    cur = conn.cursor()

    for i in range(1, 101):
        print(i)
        sql = "INSERT INTO public.instagram (id) VALUES (%s, " \
              "%s,%s, %s," \
              "%s, %s, %s, %s) ON CONFLICT ON CONSTRAINT instagram_pk DO UPDATE set " \
              "following = EXCLUDED.following,  " \
              "followers = EXCLUDED.followers , " \
              "bio = EXCLUDED.bio , " \
              "profile_pic_url = EXCLUDED.profile_pic_url,  " \
              "business_category_name = EXCLUDED.business_category_name , " \
              "external_url = EXCLUDED.external_url , " \
              "is_verified = EXCLUDED.is_verified  " \
              "  returning id; "



    conn.commit()


