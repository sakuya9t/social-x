from selenium import webdriver

import selenium
from selenium.webdriver.chrome.options import Options
import time

from utils import logger
from utils.AbstractParser import AbstractParser
from constant import DRIVER_PATH
from utils.InvalidAccountException import InvalidAccountException


class TwiUtils(AbstractParser):
    def __init__(self, displayed=False):
        chrome_options = Options()
        if not displayed:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome(DRIVER_PATH, options=chrome_options)
        self.browser.set_window_size(1920, 1080)

    def isSuspended(self):
        page_text = self.browser.find_elements_by_tag_name("body")[0].text
        return "Account suspended" in page_text

    def isProtected(self):
        page_text = self.browser.find_elements_by_tag_name("body")[0].text
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
        self.browser.get("https://www.twitter.com/" + username)
        time.sleep(3)

        y_offset = 0
        d_height = 0
        post_text = set()
        err_count = 0
        while True:
            texts = []
            try:
                elements = self.browser.find_elements_by_css_selector("[lang]")[1:]
                texts = [x.text for x in elements]
            except:
                err_count += 1
                time.sleep(0.5)
                if err_count > 20:
                    pass
            post_text.update(texts)
            self.browser.execute_script("window.scrollBy(0,2000)")
            y_pos = self.browser.execute_script("return window.pageYOffset")
            curr_height = self.browser.execute_script("return document.body.scrollHeight")
            if y_pos == y_offset and d_height == curr_height:
                break
            d_height = curr_height
            y_offset = y_pos
            time.sleep(0.1)
            if len(post_text) > 1000:
                break
        logger.info("{} tweets parsed.".format(len(post_text)))
        return list(post_text)

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
        if self.isSuspended() or self.isProtected():
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
        if self.isSuspended() or self.isProtected():
            raise InvalidAccountException('Invalid Twitter Account {}'.format(username))
        profile = self.parse_profile(username)
        posts_content = self.parse_posts(username)
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
