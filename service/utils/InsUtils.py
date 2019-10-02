import ast
import json
import re
import time

import requests
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from constant import DRIVER_PATH
from utils import logger
from utils.AbstractParser import AbstractParser
from utils.InvalidAccountException import InvalidAccountException


class InsUtils(AbstractParser):
    def __init__(self, displayed=False):
        self.chrome_options = Options()
        if not displayed:
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome(DRIVER_PATH, options=self.chrome_options)
        self.browser.set_window_size(1920, 1080)
        self.browser.get("https://www.instagram.com/")

    def is_invalid(self, username):
        url = "https://www.instagram.com/" + username
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        target_ele = soup.find_all('meta', {'property': 'og:title'})
        return len(target_ele) == 0

    def is_private_or_protected(self, username):
        url = "https://www.instagram.com/" + username
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        major_script = list(filter(lambda x: 'window._sharedData = ' in x.text, soup.find_all('script')))[0].text
        major_script = json.loads(re.findall(r'{\".*}', major_script)[0])
        is_private = major_script['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']
        is_empty = len(major_script['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']) == 0
        return is_private or is_empty

    def parse_profile(self, username):
        if self.is_invalid(username):
            raise InvalidAccountException('Invalid Instagram Account {}'.format(username))

        response = requests.get('https://www.instagram.com/{}/'.format(username))
        soup = BeautifulSoup(response.text)
        major_script = list(filter(lambda x: 'window._sharedData = ' in x.text, soup.find_all('script')))[0].text
        major_script = json.loads(re.findall(r'{\".*}', major_script)[0])
        profile_img = major_script['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd']

        user_info = json.loads(soup.find('script', {'type': 'application/ld+json'}).text.strip())
        screen_name = user_info['name']
        desc_str = user_info['description'].replace("\n", ";;")
        return {"username": screen_name, "description": desc_str, "image": profile_img}

    def parse_posts(self, username):
        self.browser.get("https://www.instagram.com/" + username + "/")
        time.sleep(3)
        a_hrefs = set()
        y_offset = 0
        while True:
            self.browser.execute_script("window.scrollBy(0,300)")
            y_pos = self.browser.execute_script("return window.pageYOffset")
            if y_pos == y_offset:
                break
            y_offset = y_pos
            mainpart = self.browser.find_elements_by_tag_name("article")[0] \
                .find_elements_by_xpath("*")[0].find_elements_by_xpath("*")[0]
            a_labels = mainpart.find_elements_by_tag_name("a")
            for a_label in a_labels:
                a_href = a_label.get_attribute("href")
                a_hrefs.add(a_href)
            time.sleep(0.1)
        a_hrefs = list(a_hrefs)
        return a_hrefs[:500]

    def get_post_content(self, url):
        resp = requests.get(url)
        data = resp.text
        soup = BeautifulSoup(data)
        text = soup.find_all("title")[0].get_text()
        matches = re.findall(r'“(.+?)”', text)
        script_text = list(filter(lambda x: 'display_url' in x.get_text(), soup.find_all("script")))[0].get_text()
        url_json = ast.literal_eval('{' + re.findall(r'\"display_url\":\"[^\"]*\"', script_text)[0] + '}')
        image_url = re.sub('&.*', '', url_json['display_url'])
        if len(matches) == 0:
            post_text = ""
        else:
            post_text = matches[0]
        return {"text": post_text, "image": image_url}


class InsUtilsNoLogin(InsUtils):
    def parse(self, username):
        if self.is_invalid(username):
            raise InvalidAccountException('Invalid Instagram Account {}'.format(username))
        profile = self.parse_profile(username)
        logger.info("Parse Instagram profile {} succeed.".format(username))
        if self.is_private_or_protected(username):
            return {"profile": profile, "posts_content": []}
        posts_urls = self.parse_posts(username)
        logger.info(
            "Parse Instagram account {} posts url succeed, ".format(username) + str(len(posts_urls)) + " posts.")
        posts_content = self.multi_thread_parse(callback=self.get_post_content, urls=posts_urls)
        logger.info('Parse Instagram Account {} successful.'.format(username))
        return {"profile": profile, "posts_content": posts_content}


class InsUtilsWithLogin(InsUtils):
    def login(self, account):
        loginurl = 'https://www.instagram.com/accounts/login/'
        self.browser.get(loginurl)
        time.sleep(3)
        # sign in the username and pass
        inputs = self.browser.find_elements_by_tag_name("input")
        username, password = account
        inputs[0].send_keys(username)
        inputs[1].send_keys(password)

        # click to login
        btn = self.browser.find_elements_by_tag_name("button")[1]
        btn.click()
        time.sleep(3)
        return self.browser.current_url != 'https://www.instagram.com/accounts/login/'

    def parse_network(self, username):
        self.browser.get("https://www.instagram.com/" + username + "/")
        sub_window_container = self.browser.find_element_by_css_selector("[role=\"dialog\"]") \
            .find_elements_by_xpath("*")[2]
        length = 0
        lis = sub_window_container.find_elements_by_tag_name("li")
        li_length = len(lis)

        while li_length > length:
            length = li_length
            for i in range(50):
                self.browser.execute_script("arguments[0].scrollBy(0,100);", sub_window_container)
                time.sleep(0.1)
            lis = sub_window_container.find_elements_by_tag_name("li")
            li_length = len(lis)

        follow_list = set()
        names = sub_window_container.find_elements_by_css_selector("[title]")
        for name in names:
            follow_list.add(name.get_attribute("innerText"))
        close_button = self.browser.find_element_by_css_selector("[role=\"dialog\"]").find_elements_by_tag_name("button")[0]
        close_button.click()
        return list(follow_list)

    def turn_num(self, s):
        s = s.replace(",", "")
        unit = s[-1]
        if not str.isdigit(unit):
            i = float(s[:-1])
            if unit == "k":
                i *= 1000
            elif unit == "M":
                i *= 1000000
        else:
            i = int(s)
        return int(i)

    def parse(self, username):
        if self.is_invalid(username):
            raise InvalidAccountException('Invalid Instagram Account {}'.format(username))
        profile = self.parse_profile(username)
        logger.info("Parse Instagram profile {} succeed.".format(username))
        if self.is_private_or_protected(username):
            return {"profile": profile, "posts_content": []}
        following = self.parse_network(username)
        logger.info(
            "Parse Instagram account {} following succeed, ".format(username) + str(len(following)) + " followings.")
        posts_urls = self.parse_posts(username)
        logger.info(
            "Parse Instagram account {} posts url succeed, ".format(username) + str(len(posts_urls)) + " posts.")
        posts_content = self.multi_thread_parse(callback=self.get_post_content, urls=posts_urls)
        return {"profile": profile, "following": following, "posts_content": posts_content}


def find_post_owner(url):
    resp = requests.get(url)
    data = resp.text
    soup = BeautifulSoup(data)
    text = soup.find_all("script", {"type": "application/ld+json"})[0].text
    username = ast.literal_eval(re.sub(r'[\n ]', "", text))['author']['alternateName'].replace('@', '')
    return username


def is_valid_instagram_data(content):
    if 'posts_content' not in content.keys():
        return 'profile' in content.keys() and 'status' in content['profile'].keys()
    return True
