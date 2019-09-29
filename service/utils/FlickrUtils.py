import selenium
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
from multiprocessing.dummy import Pool as ThreadPool
from constant import DRIVER_PATH
from utils.AbstractParser import AbstractParser


class FlickrUtils(AbstractParser):
    def __init__(self, displayed=False):
        chrome_options = Options()
        if not displayed:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome(DRIVER_PATH, options=chrome_options)
        self.browser.set_window_size(1920, 1080)
    
    def set_user(self, username):
        self.username = username
        self.base_url = 'https://www.flickr.com/'
        self.links = {'about': 'people/{}'.format(username), 
                      'photostream': 'photos/{}'.format(username), 
                      'following': 'people/{}/contacts'.format(username),
                      'groups': 'people/{}/groups'.format(username)}

    def parse(self, username):
        self.set_user(username)
        profile = self.parse_profile(username)
        posts = self.multi_thread_parse(callback=self.get_post_content, urls=self.parse_image_urls())
        following = self.get_followings()
        groups = self.get_user_groups()
        return {"profile": profile, "posts_content": posts, "following": following, "groups": groups}

    def next_page(self):
        try:
            pager = self.browser.find_element_by_class_name("pagination-view")
            next_page_link = pager.find_element_by_css_selector("[rel=\"next\"]")
            next_page_link.click()
            return True
        except NoSuchElementException:
            return False

    def parse_image_urls(self):
        self.browser.get(self.base_url + self.links['photostream'])
        has_more = True
        image_urls = []
        while has_more:
            time.sleep(5)
            self.browser.execute_script("window.scrollBy(0,30000)")
            time.sleep(5)
            photo_elements = self.browser.find_elements_by_class_name("photo-list-photo-interaction")
            photo_elements = [x.find_element_by_class_name("overlay") for x in photo_elements]
            urls = [x.get_attribute("href") for x in photo_elements]
            image_urls += urls
            has_more = self.next_page()
        return image_urls

    def get_post_content(self, url):
        resp = requests.get(url)
        data = resp.text
        soup = BeautifulSoup(data)
        image = 'https:' + soup.find("img", {"class": "main-photo"})['src']
        image = image[:-4] + "_b" + ".jpg"
        description = soup.find("meta", {"name":"description"})['content']
        title = soup.find("meta", {"name":"title"})['content']
        return {'title': title, 'desc': description, 'image': image}

    def get_followings(self):
        self.browser.get(self.base_url + self.links['following'])
        following_ids = []
        while True:
            try:
                elements = self.browser.find_elements_by_css_selector(".Icon [rel=contact]")
                following_ids += [x.get_attribute('href').split("/")[-2] for x in elements]
                next_button = self.browser.find_element_by_css_selector("[data-track=next]")
                next_button.click()
                time.sleep(3)
            except:
                break
        return following_ids

    def parse_profile(self, username):
        self.set_user(username)
        profile = {'username': username}
        resp = requests.get(self.base_url + self.links['about'])
        data = resp.text
        soup = BeautifulSoup(data)
        image_property = "https:" + re.findall(r'\(.+\?', soup.find("div", {"class": "avatar"})['style'])[0][1:-1]
        profile['image'] = image_property
        screen_name = soup.find("h1", {"class": "truncate"}).get_text().strip()
        profile['screen_name'] = screen_name
        desc_component = soup.find("div", {"class": "description"})
        if desc_component:
            desc_text = desc_component.get_text()
            desc_link = [x['href'] for x in desc_component.find_all('a')]
            profile['description'] = desc_text
            profile['links'] = desc_link
        return profile

    def get_user_groups(self):
        self.browser.get(self.base_url + self.links['groups'])
        time.sleep(2)
        trs = self.browser.find_element_by_class_name("main").find_elements_by_tag_name("tr")[1:]
        group_names = [x.find_element_by_css_selector("td:nth-child(1)").find_element_by_tag_name("a").text for x in trs]
        return group_names
