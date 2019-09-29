import os
from multiprocessing.pool import ThreadPool

import psutil as psutil

THREAD_POOL_SIZE = 20


class AbstractParser:
    browser = None

    def parse_profile(self, username):
        pass

    def parse(self, username):
        pass

    def close(self):
        if self.browser:
            browser_pid = self.browser.service.process.pid
            p = psutil.Process(browser_pid)
            pids = [sub.pid for sub in p.children(recursive=True)]
            pids.append(browser_pid)
            self.browser.quit()
            for pid in pids:
                try:
                    os.system('kill -9 {}'.format(pid))
                except psutil.NoSuchProcess:
                    continue

    @staticmethod
    def multi_thread_parse(callback, urls):
        pool = ThreadPool(THREAD_POOL_SIZE)
        results = pool.map(callback, urls)
        return results
