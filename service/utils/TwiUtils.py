import requests
from bs4 import BeautifulSoup

from selenium import webdriver

import selenium
from selenium.webdriver.chrome.options import Options
import time

from utils import logger
from utils.AbstractParser import AbstractParser
from constant import DRIVER_PATH
from utils.InvalidAccountException import InvalidAccountException

THREAD_POOL_SIZE = 20


class TwiUtils(AbstractParser):
    def __init__(self, displayed=False):
        chrome_options = Options()
        if not displayed:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome(DRIVER_PATH, options=chrome_options)
        self.browser.set_window_size(1920, 1080)

    def isSuspended(self):
        page_text = self.browser.find_element_by_tag_name("body").text
        return "Account suspended" in page_text

    def notExist(self):
        page_text = self.browser.find_element_by_tag_name("body").text
        return "that page doesn’t exist" in page_text

    def isProtected(self):
        page_text = self.browser.find_element_by_tag_name("body").text
        return "This account's Tweets are protected." in page_text

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
        if self.isProtected():
            logger.info("Twitter account {name} is protected.".format(name=username))
            return None
        if self.isSuspended():
            logger.info("Twitter account {name} is suspended.".format(name=username))
            return None
        if self.notExist():
            logger.info("Twitter account {name} not exist.".format(name=username))
            return None
        self.browser.get("https://www.twitter.com/" + username)
        time.sleep(3)

        y_offset = 0
        d_height = 0
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
                if err_count > 20:
                    pass
            self.browser.execute_script("window.scrollBy(0,20000)")
            y_pos = self.browser.execute_script("return window.pageYOffset")
            curr_height = self.browser.execute_script("return document.body.scrollHeight")
            if y_pos == y_offset and d_height == curr_height:
                break
            d_height = curr_height
            y_offset = y_pos
            time.sleep(0.3)
            if len(post_ids) > 1000:
                break
        post_ids = [x.split('-')[-1] for x in post_ids]
        post_urls = ['https://twitter.com/{}/status/{}'.format(username, id) for id in post_ids]
        return post_urls

    def get_post_content(self, url):
        resp = requests.get(url)
        data = resp.text
        soup = BeautifulSoup(data)
        desc_element = soup.find('meta', {'property': 'og:description'})
        description = "" if not desc_element else desc_element['content']
        images = [x['content'] for x in soup.find_all('meta', {'property': 'og:image'})]
        images = list(filter(lambda x: 'profile_images' not in x, images))
        return {'text': description, 'image': images}

    def close(self):
        self.browser.quit()


class TwiUtilsNoLogin(TwiUtils):
    def getPhoto(self, username):
        url = "https://www.twitter.com/" + username
        self.browser.get(url)
        time.sleep(3)
        try:
            image_element = self.browser.find_element_by_class_name("ProfileAvatar-image")
            img_url = image_element.get_attribute("src")
            return img_url
        except:
            return ""

    def parse_profile(self, username):
        url = "https://www.twitter.com/" + username
        self.browser.get(url)
        time.sleep(3)
        if self.isSuspended() or self.notExist():
            raise InvalidAccountException('Invalid Twitter Account {}'.format(username))
        profile_card = self.browser.find_element_by_class_name("ProfileHeaderCard")
        name = profile_card.find_element_by_class_name("ProfileHeaderCard-name").text
        screen_name = profile_card.find_element_by_class_name("ProfileHeaderCard-screenname").text
        screen_name = screen_name[1:] if screen_name[0] == '@' else screen_name
        self_desc = profile_card.find_element_by_class_name("ProfileHeaderCard-bio").text
        location = profile_card.find_element_by_class_name("ProfileHeaderCard-location").text
        conn_url = profile_card.find_element_by_class_name("ProfileHeaderCard-urlText").text
        profile_img = self.browser.find_element_by_class_name("ProfileAvatar-image").get_attribute("src")
        return {"username": screen_name, "name": name, "description": self_desc, "location": location, "url": conn_url,
                "image": profile_img}

    def parse(self, username):
        url = "https://www.twitter.com/" + username
        self.browser.get(url)
        time.sleep(3)
        if self.isSuspended() or self.notExist():
            raise InvalidAccountException('Invalid Twitter Account {}'.format(username))
        profile = self.parse_profile(username)
        if self.isProtected():
            return {"profile": profile, "posts_content": []}
        posts_urls = self.parse_posts(username)
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

    def getPhoto(self, username):
        url = "https://www.twitter.com/" + username
        self.browser.get(url)
        time.sleep(3)
        query_href = "[href=\"/{name}/photo\"]".format(name=username)
        try:
            image_element = self.browser.find_element_by_css_selector(query_href)
            img_url = image_element.find_elements_by_tag_name("img")[0].get_attribute("src")
            return img_url
        except:
            return ""
