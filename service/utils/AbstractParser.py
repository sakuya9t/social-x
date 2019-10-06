import os
from multiprocessing.pool import ThreadPool

import psutil as psutil
import requests

from constant import USER_AGENT

THREAD_POOL_SIZE = 20


class AbstractParser:
    browser = None

    def parse_profile(self, username):
        pass

    def parse(self, username):
        pass

    def close(self):
        if self.browser and self.browser.service.process:
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

    @staticmethod
    def multi_thread_parse(callback, urls):
        pool = ThreadPool(THREAD_POOL_SIZE)
        results = pool.map(callback, urls)
        return results

    @staticmethod
    def get_url(url):
        header = {'User-Agent': USER_AGENT}
        content = requests.get(url, headers=header)
        return content
