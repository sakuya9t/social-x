import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import numpy as np
from sklearn import preprocessing
import readability
import random
import string
import time


class TeaUtils:
    def __init__(self, driver):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = selenium.webdriver.Chrome(driver, options=chrome_options)
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
                
    def __del__(self):
        self.browser.close()


def query_writing_style(text, driver):
    tea_metrics = TeaUtils(driver).getTextMetrics(text)
    readbility_metrics = dict(readability.getmeasures(text, lang='en')['readability grades'])
    return {'tea': tea_metrics, 'readbility': readbility_metrics}
                
    
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def writing_style_similarity(vector1, vector2):
    tea1 = np.asarray(vector1['tea'].append(vector1['readbility'] / 10), dtype=np.float)
    tea2 = np.asarray(vector2['tea'].append(vector2['readbility'] / 10), dtype=np.float)
    vA = preprocessing.normalize(tea1, norm='l1')
    vB = preprocessing.normalize(tea2, norm='l1')
    return np.dot(vA, vB) / (np.sqrt(np.dot(vA, vA)) * np.sqrt(np.dot(vB, vB)))
