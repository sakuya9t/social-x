import time

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from constant import DRIVER_PATH
from utils import logger
from utils.AbstractParser import AbstractParser
from utils.InvalidAccountException import InvalidAccountException

THREAD_POOL_SIZE = 20
QUEUE_SIZE_THRESHOLD = 20


class TwiUtils(AbstractParser):
    def __init__(self, displayed=False):
        chrome_options = Options()
        if not displayed:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome(DRIVER_PATH, options=chrome_options)
        self.browser.set_window_size(1920, 1080)

    def isSuspendedOrInvalid(self, username):
        url = "https://www.twitter.com/" + username
        resp = self.get_url(url)
        data = resp.text
        return "This account has been suspended" in data or "that page doesn’t exist" in data

    def isProtectedOrEmpty(self, username):
        url = "https://www.twitter.com/" + username
        resp = self.get_url(url)
        data = resp.text
        return "This account's Tweets are protected." in data or "hasn't Tweeted" in data

    def login(self):
        pass

    def getPhoto(self, username):
        pass

    def parse_profile(self, username):
        pass

    def parse(self, username):
        pass

    def parse_posts(self, username):
        logger.info("Start parsing Twitter user: " + username)
        if self.isProtectedOrEmpty(username):
            logger.info("Twitter account {name} is protected or empty.".format(name=username))
            return None
        if self.isSuspendedOrInvalid(username):
            logger.info("Twitter account {name} is invalid.".format(name=username))
            return None
        self.browser.get("https://www.twitter.com/" + username)
        time.sleep(3)

        queue_window_pos = []
        queue_window_size = []
        err_count = 0
        post_ids = []
        while True:
            try:
                container = self.browser.find_element_by_class_name('stream')
                elements = container.find_elements_by_class_name('stream-item')
                post_ids = [x.get_attribute('id') for x in elements]
            except Exception as ex:
                err_count += 1
                logger.warning("Exception happened: {}, retrying {}/20...".format(ex, err_count))
                time.sleep(0.5)
                if err_count == 10:
                    self.browser.refresh()
                    time.sleep(5)
                if err_count > 20:
                    return None
            self.browser.execute_script("window.scrollBy(0,20000)")
            time.sleep(0.3)
            y_pos = self.browser.execute_script("return window.pageYOffset")
            curr_height = self.browser.execute_script("return document.body.scrollHeight")
            queue_window_pos.append(y_pos)
            if len(queue_window_pos) > QUEUE_SIZE_THRESHOLD:
                queue_window_pos.pop(0)
            queue_window_size.append(curr_height)
            if len(queue_window_size) > QUEUE_SIZE_THRESHOLD:
                queue_window_size.pop(0)
            if len(queue_window_pos) >= QUEUE_SIZE_THRESHOLD and len(queue_window_size) >= QUEUE_SIZE_THRESHOLD:
                if queue_window_pos[1:] == queue_window_pos[:-1] and queue_window_size[1:] == queue_window_size[:-1]:
                    break
            if len(post_ids) > 1000:
                break
        post_ids = [x.split('-')[-1] for x in post_ids]
        post_urls = ['https://twitter.com/{}/status/{}'.format(username, id) for id in post_ids]
        return post_urls

    def get_post_content(self, url):
        resp = self.get_url(url)
        data = resp.text
        soup = BeautifulSoup(data)
        desc_element = soup.find('meta', {'property': 'og:description'})
        description = "" if not desc_element else desc_element['content']
        images = [x['content'] for x in soup.find_all('meta', {'property': 'og:image'})]
        images = list(filter(lambda x: 'profile_images' not in x, images))
        return {'text': description, 'image': images}


class TwiUtilsNoLogin(TwiUtils):
    def parse_profile(self, username):
        if self.isSuspendedOrInvalid(username):
            raise InvalidAccountException('Invalid Twitter Account {}'.format(username))
        url = "https://www.twitter.com/" + username
        response = self.get_url(url)
        data = response.text
        soup = BeautifulSoup(data)
        self_desc_ele = soup.find('p', {'class': 'ProfileHeaderCard-bio'})
        self_desc = self_desc_ele.text if self_desc_ele else ""
        name_ele = soup.find('a', {'class': 'ProfileHeaderCard-nameLink'})
        name = name_ele.text if name_ele else ""
        screen_name_ele = soup.find('div', {'class': 'ProfileCardMini-screenname'})
        screen_name = screen_name_ele.text.strip() if screen_name_ele else ""
        location_ele = soup.find('span', {'class': 'ProfileHeaderCard-locationText'})
        location = location_ele.text if location_ele else ""
        url_ele = soup.find('span', {'class': 'ProfileHeaderCard-urlText'}).find('a')
        conn_url = url_ele['title'] if url_ele else ""
        img_ele = soup.find('img', {'class': 'ProfileAvatar-image'})
        profile_img = img_ele.text if img_ele else ""
        return {"username": screen_name, "name": name, "description": self_desc, "location": location, "url": conn_url,
                "image": profile_img}

    def parse(self, username):
        if self.isSuspendedOrInvalid(username):
            raise InvalidAccountException('Invalid Twitter Account {}'.format(username))
        profile = self.parse_profile(username)
        if self.isProtectedOrEmpty(username):
            return {"profile": profile, "posts_content": []}
        posts_urls = self.parse_posts(username)
        if posts_urls is None:
            raise ValueError('Exception happened when parsing Twitter account {}'.format(username))
        logger.info(
            "Parse Twitter account {} posts url succeed, ".format(username) + str(len(posts_urls)) + " posts.")
        posts_content = self.multi_thread_parse(callback=self.get_post_content, urls=posts_urls)
        logger.info('Parse Twitter Account {} successful.'.format(username))
        return {"profile": profile, "posts_content": posts_content}


class TwiUtilsWithLogin(TwiUtils):
    def set_account(self, account):
        self.account = account

    def login(self):
        self.browser.get("https://twitter.com/login")
        time.sleep(3)
        inputs = self.browser.find_elements_by_tag_name("fieldset")[0].find_elements_by_tag_name("input")
        username, password = self.account
        inputs[0].send_keys(username)
        inputs[1].send_keys(password)
        submit_button = self.browser.find_element_by_css_selector("button.submit")
        submit_button.click()
        time.sleep(3)
        return "login" not in self.browser.current_url
