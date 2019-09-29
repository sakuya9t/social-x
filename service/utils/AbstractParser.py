from multiprocessing.pool import ThreadPool

THREAD_POOL_SIZE = 20


class AbstractParser:
    def parse_profile(self, username):
        pass

    def parse(self, username):
        pass

    def close(self):
        pass

    def multi_thread_parse(self, callback, urls):
        pool = ThreadPool(THREAD_POOL_SIZE)
        results = pool.map(callback, urls)
        return results
