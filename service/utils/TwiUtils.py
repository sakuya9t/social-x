import selenium
from selenium import webdriver

import selenium
from selenium.webdriver.chrome.options import Options
import time
import sys

class TwiUtils:
    def __init__(self, login):
        if login:
            self.twitter = TwiUtilsWithLogin()
        else:
            self.twitter = TwiUtilsNoLogin()
            
    def isSuspended(self, username):
        return self.twitter.isSuspended(username)
    
    def isProtected(self, username):
        return self.twitter.isProtected(username)
    
    def getPhoto(self, username):
        return self.twitter.getPhoto(username)
        
    def parse_profile(self, username):
        return self.twitter.parse_profile(username)
        
    def parse(self, username):
        return self.twitter.parse(username)
        
    def parse_posts(self, username):
        return self.twitter.parse_posts(username)
        
    def close(self):
        self.twitter.close()

class TwiUtilsNoLogin:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome('./chromedriver', options=chrome_options)
        self.browser.set_window_size(1920, 1080)
        
    def isSuspended(self, username):
        url = "https://www.twitter.com/" + username
        self.browser.get(url)
        time.sleep(3)
        page_text = self.browser.find_elements_by_tag_name("body")[0].text
        return "Account suspended" in page_text
    
    def isProtected(self, username):
        url = "https://www.twitter.com/" + username
        self.browser.get(url)
        time.sleep(3)
        page_text = self.browser.find_elements_by_tag_name("body")[0].text
        return "This account's Tweets are protected." in page_text
    
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
        profile_card = self.browser.find_element_by_class_name("ProfileHeaderCard")
        name = profile_card.find_element_by_class_name("ProfileHeaderCard-name").text
        screen_name = profile_card.find_element_by_class_name("ProfileHeaderCard-screenname").text
        self_desc = profile_card.find_element_by_class_name("ProfileHeaderCard-bio").text
        location = profile_card.find_element_by_class_name("ProfileHeaderCard-location").text
        conn_url = profile_card.find_element_by_class_name("ProfileHeaderCard-urlText").text
        profile_img = self.browser.find_element_by_class_name("ProfileAvatar-image").get_attribute("src")
        return {"username": screen_name, "name": name, "description": self_desc, "location": location, "url": conn_url, "image": profile_img}
        
    def parse(self, username):
        if self.isSuspended(username):
            return {}
        profile = self.parse_profile(username)
        posts_content = self.parse_posts(username)
        return {"profile": profile, "posts_content": posts_content}
    
    def parse_posts(self, username):
        print("Parsing tweets of user: " + username)
        page_text = self.browser.find_elements_by_tag_name("body")[0].text
        if "This account's Tweets are protected." in page_text:
            print("Account {name} is protected.".format(name=username))
            return []
        self.browser.get("https://www.twitter.com/" + username)
        time.sleep(3)
        
        y_offset = 0
        d_height = 0
        post_text = set()
        while True:
            try:
                elements = self.browser.find_elements_by_css_selector("[lang]")[1:]
                texts = [x.text for x in elements]
            except:
                time.sleep(0.5)
                continue
            post_text.update(texts)
            self.browser.execute_script("window.scrollBy(0,2000)")
            y_pos = self.browser.execute_script("return window.pageYOffset")
            curr_height = self.browser.execute_script("return document.body.scrollHeight")
            if y_pos == y_offset and d_height == curr_height:
                break
            d_height = curr_height
            y_offset = y_pos
            time.sleep(0.1)
            print('{} tweets parsed.'.format(len(post_text)), end='\r')
            sys.stdout.flush()
            if len(post_text) > 1000:
                break
        return list(post_text)
    
    def close(self):
        self.browser.stop_client()
        self.browser.close()


class TwiUtilsWithLogin:

    def __init__(self, displayed):
        chrome_options = Options()
        if not displayed:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome('./chromedriver', options=chrome_options)
        self.browser.set_window_size(1920, 1080)

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
        
    def isSuspended(self, username):
        url = "https://www.twitter.com/" + username
        self.browser.get(url)
        time.sleep(3)
        page_text = self.browser.find_elements_by_tag_name("body")[0].text
        return "Account suspended" in page_text
    
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
        
    def parse_posts(self, username):
        print("Parsing tweets of user: " + username)
        self.browser.get("https://www.twitter.com/" + username)
        time.sleep(3)
        
        y_offset = 0
        d_height = 0
        post_text = set()
        err_count = 0
        while True:
            try:
                elements = self.browser.find_elements_by_css_selector("[lang]")[1:]
                texts = [x.text for x in elements]
                err_count = 0
            except:
                err_count += 1
                time.sleep(0.5)
                if(err_count > 20):
                    break
                continue
            post_text.update(texts)
            self.browser.execute_script("window.scrollBy(0,2000)")
            y_pos = self.browser.execute_script("return window.pageYOffset")
            curr_height = self.browser.execute_script("return document.body.scrollHeight")
            if y_pos == y_offset and d_height == curr_height:
                break
            d_height = curr_height
            y_offset = y_pos
            time.sleep(0.1)
            print('{} tweets parsed.'.format(len(post_text)), end='\r')
            sys.stdout.flush()
            if len(post_text) > 1000:
                break
        return list(post_text)
    
    def close(self):
        self.browser.stop_client()
        self.browser.close()