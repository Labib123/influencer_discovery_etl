import time
from telnetlib import EC
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

# Create Empty List

link = []
names = []

# login first

driver = webdriver.Chrome(executable_path="./chromedriver")

driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)
username = driver.find_element_by_name('username')
username.send_keys('yourUsername')
password = driver.find_element_by_name('password')
password.send_keys('yourPassword')
#instead of searching for the Button (Log In) you can simply press enter when you already selected the password or the username input element.
submit = driver.find_element_by_tag_name('form')
submit.submit()

# Function to get Post Link
def get_influencer_link(username):
    # to influencer url
    url = f'https://www.instagram.com/{username}/'
    driver.get(url)
    time.sleep(5)
    i = 0
    while i < 8:
        try:
            # get the links
            pages = driver.find_elements_by_tag_name('a')
            for data in pages:
                data_2 = data.get_attribute("href")
                if '/p/' in data_2:
                    link.append(data.get_attribute("href"))
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(1)
            i += 1
        except:
            i += 1
            continue
    print(len(link))
    driver.quit()


get_influencer_link('afshaa17')
