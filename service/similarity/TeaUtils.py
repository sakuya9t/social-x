from multiprocessing.pool import ThreadPool
from constant import DRIVER_PATH, ALGOCONFIG_PATH

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import readability
import random
import string
import time

from similarity.Config import Config


class TeaUtils:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome(DRIVER_PATH, options=chrome_options)
        self.browser.set_window_size(1920, 1080)
        self.login()
        
    def login(self):
        retry = True
        while retry:
            self.browser.get("http://141.225.41.245/cohmetrixgates/")
            try:
                err_element = self.browser.find_element_by_id("main-frame-error")
                time.sleep(5)
            except NoSuchElementException as e:
                retry = False
        inputbox = self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtUserName")
        submitbtn = self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_btnLogin")
        inputbox.send_keys(randomString())
        submitbtn.click()
        time.sleep(3)
        
    def getTextMetrics(self, text):
        try:
            textbox = self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtMultiLine")
            submitbtn = self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_btnAnalyse")
            textbox.send_keys(text)
            submitbtn.click()
            table = self.getResultTable()
            metrics = table.text
            info = dict((x, y) for x, y in (zip(metrics.splitlines()[0:5], [int(x[:-1]) / 100 for x in metrics.splitlines()[5:10]])))
            info[str.join(" ", metrics.splitlines()[11].split(" ")[:-1])] = float(metrics.splitlines()[11].split(" ")[-1])
            return info
        except NoSuchElementException:
            self.browser.refresh()
            time.sleep(5)
        
    def getResultTable(self):
        while True:
            try:
                target = self.browser.find_element_by_id("ctl00_ContentPlaceHolder1_tblChart")
                return target
            except Exception as e:
                time.sleep(5)
                continue

    def close(self):
        self.browser.quit()


tea_enabled = bool(Config(ALGOCONFIG_PATH).get('tea-enabled'))


def query_writing_style(text):
    text = ''.join(c for c in text if c <= '\uFFFF')
    readbility_metrics = dict(readability.getmeasures(text, lang='en')['readability grades'])
    if tea_enabled:
        text = ' '.join(text.split(' ')[:300])
        tea = TeaUtils()
        tea_metrics = tea.getTextMetrics(text)
        tea.close()
        return {'tea': tea_metrics, 'readbility': readbility_metrics}
    else:
        return {'readbility': readbility_metrics}


def multi_thread_query_writing_style(texts, n_threads):
    pool = ThreadPool(n_threads)
    results = pool.map(query_writing_style, texts)
    return results
                
    
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def writing_style_similarity(vector1, vector2):
    read1 = np.asarray(list(vector1['readbility'].values()), dtype=np.float)
    read1 = np.true_divide(read1, np.linalg.norm(read1))
    read2 = np.asarray(list(vector2['readbility'].values()), dtype=np.float)
    read2 = np.true_divide(read2, np.linalg.norm(read2))
    if not tea_enabled:
        return [cosine_similarity(read1, read2)]
    value1 = list(vector1['tea'].values())[:-1]
    value1.append(vector1['tea']['Flesch Kincaid Grade Level'] / 10)
    value2 = list(vector2['tea'].values())[:-1]
    value2.append(vector2['tea']['Flesch Kincaid Grade Level'] / 10)
    tea1 = np.asarray(value1, dtype=np.float)
    tea1 = np.true_divide(tea1, np.linalg.norm(tea1))
    tea2 = np.asarray(value2, dtype=np.float)
    tea2 = np.true_divide(tea2, np.linalg.norm(tea2))
    return [cosine_similarity(tea1, tea2), cosine_similarity(read1, read2)]


def cosine_similarity(vA, vB):
    return np.dot(vA, vB) / (np.sqrt(np.dot(vA, vA)) * np.sqrt(np.dot(vB, vB)))
