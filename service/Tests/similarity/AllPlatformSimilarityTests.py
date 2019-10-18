import unittest

from constant import REALTIME_MODE, DATABASE_DATA_AWAIT_FEEDBACK, BATCH_MODE
from similarity.SimCalculator import SimCalculator
from utils.QueryGenerator import retrieve


class AllPlatformSimilarityTests(unittest.TestCase):
    def test_twitter_instagram(self):
        handler = SimCalculator()
        account1 = {'platform': 'twitter', 'account': '1angharad_rees'}
        account2 = {'platform': 'instagram', 'account': 'kaligraphicprint'}
        info1 = retrieve(account1, BATCH_MODE)
        info2 = retrieve(account2, BATCH_MODE)
        info1['platform'] = account1['platform'].lower()
        info2['platform'] = account2['platform'].lower()
        vector = handler.calc(info1, info2, enable_networking=False, mode=BATCH_MODE)
        doc_id = handler.store_result(info1, info2, vector, DATABASE_DATA_AWAIT_FEEDBACK)
        self.assertIsNotNone(doc_id)

    def test_twitter_twitter(self):
        handler = SimCalculator()
        account1 = {'platform': 'twitter', 'account': '1angharad_rees'}
        account2 = {'platform': 'twitter', 'account': 'ClassicVines1'}
        info1 = retrieve(account1, BATCH_MODE)
        info2 = retrieve(account2, BATCH_MODE)
        info1['platform'] = account1['platform'].lower()
        info2['platform'] = account2['platform'].lower()
        vector = handler.calc(info1, info2, enable_networking=False, mode=BATCH_MODE)
        doc_id = handler.store_result(info1, info2, vector, DATABASE_DATA_AWAIT_FEEDBACK)
        self.assertIsNotNone(doc_id)

    def test_twitter_pinterest(self):
        handler = SimCalculator()
        account1 = {'platform': 'twitter', 'account': 'ClassicVines1'}
        account2 = {'platform': 'pinterest', 'account': 'mariesbazaar'}
        info1 = retrieve(account1, BATCH_MODE)
        info2 = retrieve(account2, BATCH_MODE)
        info1['platform'] = account1['platform'].lower()
        info2['platform'] = account2['platform'].lower()
        vector = handler.calc(info1, info2, enable_networking=False, mode=BATCH_MODE)
        doc_id = handler.store_result(info1, info2, vector, DATABASE_DATA_AWAIT_FEEDBACK)
        self.assertIsNotNone(doc_id)

    def test_instagram_flickr(self):
        handler = SimCalculator()
        account1 = {'platform': 'instagram', 'account': 'photographynadia'}
        account2 = {'platform': 'flickr', 'account': 'nadiaphotograhy'}
        info1 = retrieve(account1, BATCH_MODE)
        info2 = retrieve(account2, BATCH_MODE)
        info1['platform'] = account1['platform'].lower()
        info2['platform'] = account2['platform'].lower()
        vector = handler.calc(info1, info2, enable_networking=False, mode=BATCH_MODE)
        doc_id = handler.store_result(info1, info2, vector, DATABASE_DATA_AWAIT_FEEDBACK)
        self.assertIsNotNone(doc_id)


if __name__ == '__main__':
    unittest.main()
