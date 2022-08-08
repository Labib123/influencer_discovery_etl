import json
import time
from datetime import datetime
from instaloader import Instaloader, Profile, ProfileNotExistsException
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect
import os
import sys

CURRENT_DATE = datetime.today().strftime('%Y-%m-%d').replace("-", "")

CONFIGS = {}
raw_path = "../s3_local/raw/instagram"
raw_file = "{0}/ig_meta_{1}.json".format(raw_path, CURRENT_DATE)

loader = Instaloader()

try:
    from instaloader import ConnectionException, Instaloader
except ModuleNotFoundError:
    raise SystemExit("Instaloader not found.\n  pip install [--user] instaloader")


def get_cookiefile():
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
    return cookiefiles[0]


def import_session(cookiefile, sessionfile):
    print("Using cookies from {}.".format(cookiefile))
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )
    instaloader = Instaloader(max_connection_attempts=1)
    instaloader.context._session.cookies.update(cookie_data)
    username = instaloader.test_login()
    if not username:
        raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
    print("Imported session cookie for {}.".format(username))
    instaloader.context.username = username
    instaloader.save_session_to_file(sessionfile)


def get_profiles(profile, is_raw=False):
    with open("../s3_local/config/ig_profiles.json", 'r') as f:
        profiles = json.load(f)['profiles']
        profile_idx = profiles.index(profile)
        if is_raw:
            return profiles[profile_idx + 1:]

    return profiles[profile_idx:]


def get_latest_profile(file):
    with open(file, 'r') as f:
        profiles = json.load(f)['data']
        latest_profile = get_profiles(profiles[-1]['id'], is_raw=True)
        return latest_profile


def login():
    with open("../s3_local/config/ig_dev_accounts.json", "r") as rf:
        accounts = json.load(rf)

        for idx in accounts:
            account = accounts[idx]
            if account['consumed'] is False:
                username = account['username']
                password = account['password']
                account['resumed'] = True
                with open("../s3_local/config/ig_dev_accounts.json", 'w') as uf:
                    json.dump(accounts, uf)

                print("Logged in using {} account".format(username.split("@")[0]))

                return loader.login(username, password)


def get_meta(username):
    try:

        profile = Profile.from_username(loader.context, username)

    except ProfileNotExistsException:
        print("Oops!, Profile is not exist")
        return

    user = {}

    user['id'] = profile.username
    user['followers'] = profile.followers
    user['following'] = profile.followees
    user['bio'] = profile.biography
    user['profile_pic_url'] = profile.profile_pic_url
    user['business_category_name'] = profile.business_category_name if profile.business_category_name else "not given"
    user['media_count'] = profile.mediacount
    user['external_url'] = profile.external_url
    user['is_verified'] = profile.is_verified

    user['full_name'] = profile.full_name

    user['is_business_account'] = profile.is_business_account

    print(user)

    return user


def extract():
    with open('../s3_local/config/ig_profiles.json', 'r') as pro_f, open(
            raw_file, 'w+') as raw_f:
        # if raw_f.read(2) == '':
        if os.path.exists(raw_file):
            print("Raw file is empty ")
            raw_data = {"data": []}
            profiles_ids = json.load(pro_f)
            last_profile = profiles_ids['profiles'][0]
            profiles = get_profiles(last_profile)
            meta = get_meta(profiles[0])
            raw_data['data'].append(meta)
            with open(raw_file, 'w') as sf:
                json.dump(raw_data, sf)

        profiles = get_latest_profile(raw_file)

        for idx, profile in enumerate(profiles):
            print("Loading {} profile meta".format(profile))
            meta = get_meta(profile)
            print("successfully updated {} profile meta".format(meta['id']))
            time.sleep(2)
            print("Saving {} profile meta to S3".format(meta['id']))

            with open(raw_file, 'r') as cf:

                cashing_data = json.load(cf)['data']

            with open(raw_file, 'w') as sf:
                cashing_data.append(meta)
                raw_obj = {"data": cashing_data}
                json.dump(raw_obj, sf)
            print("successfully saved {} profile summary to S3 ".format(meta['id']))

            if idx == 20:
                login()
                idx = 0


if __name__ == "__main__":
    # p = ArgumentParser()
    # p.add_argument("-c", "--cookiefile")
    # p.add_argument("-f", "--sessionfile")
    # args = p.parse_args()
    # try:
    #     login()
    #     import_session(args.cookiefile or get_cookiefile(), args.sessionfile)
    # except (ConnectionException, OperationalError) as e:
    #     raise SystemExit("Cookie import failed: {}".format(e))
    login()
    extract()
