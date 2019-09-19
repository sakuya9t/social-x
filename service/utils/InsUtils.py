import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import requests
import re, json
from constant import DRIVER_PATH
from utils.AbstractParser import AbstractParser


class InsUtils(AbstractParser):
    def __init__(self, displayed=False):
        self.chrome_options = Options()
        if not displayed:
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome(DRIVER_PATH, options=self.chrome_options)
        self.browser.set_window_size(1920, 1080)
        self.browser.get("https://www.instagram.com/")

    def parse_profile_img(self):
        ele = self.browser.find_elements_by_tag_name("header")[0].find_elements_by_tag_name("img")[0]
        return ele.get_attribute('src')

    def parse_posts(self):
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
        url_json = json.loads('{' + re.findall(r'\"display_url\":\"[^\"]*\"', script_text)[0] + '}')
        image_url = re.sub('&.*', '', url_json['display_url'])
        if len(matches) == 0:
            post_text = ""
        else:
            post_text = matches[0]
        return {"text": post_text, "image": image_url}

    def multi_thread_parse(self, urls):
        pool = ThreadPool(10)
        results = pool.map(self.get_post_content, urls)
        return results

    def close(self):
        self.browser.stop_client()
        self.browser.close()


class InsUtilsNoLogin(InsUtils):
    def parse_profile(self, username):
        self.browser.get("https://www.instagram.com/" + username + "/")
        time.sleep(3)
        try:
            is_404 = len(self.browser.find_elements_by_class_name("dialog-404")) != 0
            if is_404:
                print("User " + username + " not exist.")
                return "INVALID"
            screen_name = self.browser.find_elements_by_tag_name("h1")[0].text
            profile_img = self.parse_profile_img()
            is_private = "This Account is Private" in self.browser.find_elements_by_tag_name("body")[0].text
            is_empty_account = "No Posts Yet" in self.browser.find_elements_by_tag_name("body")[0].text
            desc_div = self.browser.find_elements_by_tag_name("section")[1].find_elements_by_tag_name("div")[1]
            desc_str = desc_div.get_attribute("innerText")
            desc_str = desc_str.replace("\n", ";;")
            if is_private:
                print("User " + screen_name + " is a private account.")
                return {"username": screen_name, "status": "PRIVATE", "description": desc_str, "image": profile_img}
            if is_empty_account:
                print("User " + screen_name + " is an empty account.")
                return {"username": screen_name, "status": "EMPTY", "description": desc_str, "image": profile_img}
            time.sleep(3)

            return {"username": screen_name, "description": desc_str, "image": profile_img}
        except Exception as ex:
            print(str(ex))
            return "INVALID"

    def parse(self, username):
        profile = self.parse_profile(username)
        if profile == 'INVALID':
            print("Instagram account " + username + " is not available.")
            return "INVALID"
        print("Parse profile succeed.")
        if "status" in profile.keys() and profile["status"] in ["PRIVATE", "EMPTY"]:
            return {"profile": profile}
        posts_urls = self.parse_posts()
        print("Parse posts url succeed, " + str(len(posts_urls)) + " posts.")
        posts_content = self.multi_thread_parse(posts_urls)
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

    def parse_profile(self, username):
        self.browser.get("https://www.instagram.com/" + username + "/")
        time.sleep(3)
        try:
            is_404 = len(self.browser.find_elements_by_class_name("dialog-404")) != 0
            if is_404:
                print("User " + username + " not exist.")
                return "INVALID"
            screen_name = self.browser.find_elements_by_tag_name("h1")[0].text
            profile_img = self.parse_profile_img()
            is_private = "This Account is Private" in self.browser.find_elements_by_tag_name("body")[0].text
            is_empty_account = "No Posts Yet" in self.browser.find_elements_by_tag_name("body")[0].text
            if is_private or is_empty_account:
                desc_div = self.browser.find_elements_by_tag_name("section")[1].find_elements_by_tag_name("div")[2]
            else:
                desc_div = self.browser.find_elements_by_tag_name("section")[1].find_elements_by_tag_name("div")[5]
            desc_str = desc_div.get_attribute("innerText")
            desc_str = desc_str.replace("\n", ";;")
            if is_private:
                print("User " + screen_name + " is a private account.")
                return {"username": screen_name, "status": "PRIVATE", "description": desc_str, "image": profile_img}
            if is_empty_account:
                print("User " + screen_name + " is an empty account.")
                return {"username": screen_name, "status": "EMPTY", "description": desc_str, "image": profile_img}
            following_btn = self.browser.find_element_by_css_selector("[href=\"/" + screen_name + "/following/\"]")
            following_num = self.turn_num(following_btn.find_elements_by_tag_name("span")[0].get_attribute("innerText"))
            follower_btn = self.browser.find_element_by_css_selector("[href=\"/" + screen_name + "/followers/\"]")
            follower_num = self.turn_num(follower_btn.find_elements_by_tag_name("span")[0].get_attribute("innerText"))
            # print("Following: " + str(following_num) + ", Followers: " + str(follower_num))
            following_btn.click()
            time.sleep(3)

            return {"username": screen_name, "following": following_num, "follower": follower_num, "description": desc_str, "image": profile_img}
        except Exception as ex:
            print(str(ex))
            return "INVALID"

    def parse_network(self):
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
        profile = self.parse_profile(username)
        if profile == 'INVALID':
            print("Instagram account " + username + " is not available.")
            return "INVALID"
        print("Parse profile succeed.")
        if "status" in profile.keys() and profile["status"] == "PRIVATE":
            return {'profile': profile}
        following = self.parse_network()
        print("Parse following succeed, " + str(len(following)) + " followings.")
        posts_urls = self.parse_posts()
        print("Parse posts url succeed, " + str(len(posts_urls)) + " posts.")
        posts_content = self.multi_thread_parse(posts_urls)
        return {"profile": profile, "following": following, "posts_content": posts_content}
