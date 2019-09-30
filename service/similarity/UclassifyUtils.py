import ast
import json
import os
import random
import string
import time

import psutil
import selenium
import requests
from selenium.webdriver.chrome.options import Options
from sklearn.metrics.pairwise import cosine_similarity

from constant import CONFIG_PATH, DRIVER_PATH
from similarity.Config import Config
from utils import logger


def uclassify_topics(text):
    try:
        keys = Config(CONFIG_PATH).get('uclassify/apikey')
        url = 'https://api.uclassify.com/v1/uClassify/Topics/classify'
        data = {'texts': [text]}
        for key in keys:
            header = {'Authorization': 'Token {}'.format(key), 'Content-Type': 'application/json'}
            response = requests.post(url=url, data=json.dumps(data), headers=header)
            if response.status_code == 200:
                resp_data = ast.literal_eval(response.text)[0]['classification']
                res = {x['className']: x['p'] for x in resp_data}
                return res
        raise UclassifyKeyExceedException('All uClassify keys daily usage exceed.')
    except Exception as ex:
        logger.error('Error when uClassifying text: {}'.format(ex))


def uclassify_similarity(text1, text2):
    topics1 = uclassify_topics(text1)
    topics2 = uclassify_topics(text2)
    keys = set().union(topics1, topics2)
    vec1 = [topics1.get(key, 0) for key in keys]
    vec2 = [topics2.get(key, 0) for key in keys]
    return cosine_similarity([vec1], [vec2])[0][0]


class UclassifyKeyExceedException(Exception):
    pass


class UclassifyKeyGenerator:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome(DRIVER_PATH, options=chrome_options)
        self.browser.set_window_size(1920, 1080)
        self.browser.set_page_load_timeout(1800)
        self.browser.set_script_timeout(1800)

    def get_key(self):
        register_url = 'https://www.uclassify.com/account/register'
        self.browser.get(register_url)
        time.sleep(3)
        username_box = self.browser.find_element_by_id('Username')
        email_box = self.browser.find_element_by_id('Email')
        password_box = self.browser.find_element_by_id('Password')
        password_box2 = self.browser.find_element_by_id('ConfirmPassword')
        submit_btn = self.browser.find_element_by_class_name('btn')
        username = randomString()
        password = randomPassword()
        username_box.send_keys(username)
        email_box.send_keys('{}@gmail.com'.format(username))
        password_box.send_keys(password)
        password_box2.send_keys(password)
        submit_btn.click()
        time.sleep(3)
        api_key_url = 'https://www.uclassify.com/manage/apikeys'
        self.browser.get(api_key_url)
        read_key_box = self.browser.find_element_by_class_name('well')
        return read_key_box.text

    def close(self):
        browser_pid = self.browser.service.process.pid
        p = psutil.Process(browser_pid)
        pids = [sub.pid for sub in p.children(recursive=True)]
        pids.append(browser_pid)
        self.browser.quit()
        for pid in pids:
            try:
                os.system('kill -9 {} > /dev/null 2>&1'.format(pid))
            except psutil.NoSuchProcess:
                continue


def generate_uclassify_key():
    u = UclassifyKeyGenerator()
    api_key = u.get_key()
    u.close()
    logger.info('Generated uClassify api key: {}'.format(api_key))
    return api_key


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def randomPassword(stringLength=8):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    digit_part = ''.join(random.choice(string.digits))
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength - 1)) + digit_part
