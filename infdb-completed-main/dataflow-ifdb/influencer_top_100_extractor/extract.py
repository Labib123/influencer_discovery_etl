import requests as r
from bs4 import BeautifulSoup
import locale
import json
import time
from datetime import datetime

platforms = ["instagram", "tiktok", "twitch", "twitter","youtube"]


def save_to_json(data):
    with open('../s3_local/inf_data.json', 'w') as f:
        json.dump(data, f)


def extract():
    json_obj = {}

    for platform in platforms:

        print("Loading: 100 {} profiles ".format(platform))

        data = []

        time.sleep(2)

        json_obj[platform] = {}
        json_obj[platform]['data'] = data

        url = 'https://www.socialtracker.io/toplists/top-100-{0}-users-by-followers/'.format(platform)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        wp = r.get(url, headers=headers).text
        soup = BeautifulSoup(wp, 'html.parser')

        influncers = soup.find("table", {"class": 'uk-table uk-table-striped uk-text-nowrap user-table uk-table-hover'})

        table_body = influncers.find('tbody')

        rows = table_body.find_all('tr')

        for row in rows:

            cols = row.find_all('td')
            user_id = cols[2].a['href'].split('/')[2]
            cols = [ele.text.strip() for ele in cols]
            inf = [ele for ele in cols if ele] # Get rid of empty values
            inf.insert(0, user_id)
            inf.append(platform)
            data.append(inf)
        print("Uploading {0} {1} profiles: {2}".format(len(data), platform, datetime.now()))
        json_obj[platform]['data'] = data

    save_to_json(json_obj)

    # print(influncers)
    # pages = int(pages.split()[3])
    # row_collector = []
    # progress = tqdm(range(1, pages))
    # for page in progress:
    #     p_url = 'https://www.trackalytics.com/the-most-followed-instagram-profiles/page/' + str(page) + '/'
    #     tp = r.get(p_url, headers=headers).text
    #     tsoup = BeautifulSoup(tp, 'html.parser')
    #     rows = tsoup.findAll("tr")
    #     for row in range(1, 25):
    #         profile = rows[row].find(style='vertical-align:middle;width:45px;height:45px;').next_element.contents[0]
    #         followers = rows[row].find(
    #             style='vertical-align:middle;width:45px;height:45px;').next_element.next_element.next_element.next_element.contents[
    #             0].split()[0]
    #         followers = locale.atoi(followers)
    #         temp = [profile, followers]
    #         row_collector.append(temp)
    #     # Enter rate limiting per page here
    # df = pd.DataFrame(row_collector)
    # df[['profile', 'followers']] = df[[0, 1]]
    # del df[0]
    # del df[1]


extract()
