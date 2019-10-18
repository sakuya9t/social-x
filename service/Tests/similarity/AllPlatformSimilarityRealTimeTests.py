import unittest

from constant import DATABASE_DATA_AWAIT_FEEDBACK, REALTIME_MODE
from similarity.SimCalculator import SimCalculator
from utils.QueryGenerator import retrieve

ins_accounts = ['naruto.edo', 'agosnisi']
twi_accounts = ['AFP', 'Gwenda']
pin_accounts = ['ulysseswt', 'rosesforyouxx']
fli_accounts = ['clocca', 'wend']


class AllPlatformSimilarityTests(unittest.TestCase):
    def test_twitter_instagram(self):
        account1 = {'platform': 'twitter', 'account': twi_accounts[0]}
        account2 = {'platform': 'instagram', 'account': ins_accounts[0]}
        doc_id = _do_test_case(account1, account2)
        self.assertIsNotNone(doc_id)

    def test_twitter_twitter(self):
        account1 = {'platform': 'twitter', 'account': twi_accounts[0]}
        account2 = {'platform': 'twitter', 'account': twi_accounts[1]}
        doc_id = _do_test_case(account1, account2)
        self.assertIsNotNone(doc_id)

    def test_twitter_pinterest(self):
        account1 = {'platform': 'twitter', 'account': twi_accounts[0]}
        account2 = {'platform': 'pinterest', 'account': pin_accounts[0]}
        doc_id = _do_test_case(account1, account2)
        self.assertIsNotNone(doc_id)

    def test_twitter_flickr(self):
        account1 = {'platform': 'twitter', 'account': twi_accounts[0]}
        account2 = {'platform': 'flickr', 'account': fli_accounts[0]}
        doc_id = _do_test_case(account1, account2)
        self.assertIsNotNone(doc_id)

    def test_instagram_instagram(self):
        account1 = {'platform': 'instagram', 'account': ins_accounts[0]}
        account2 = {'platform': 'instagram', 'account': ins_accounts[1]}
        doc_id = _do_test_case(account1, account2)
        self.assertIsNotNone(doc_id)

    def test_instagram_pinterest(self):
        account1 = {'platform': 'instagram', 'account': ins_accounts[0]}
        account2 = {'platform': 'pinterest', 'account': pin_accounts[0]}
        doc_id = _do_test_case(account1, account2)
        self.assertIsNotNone(doc_id)

    def test_instagram_flickr(self):
        account1 = {'platform': 'instagram', 'account': ins_accounts[0]}
        account2 = {'platform': 'flickr', 'account': fli_accounts[0]}
        doc_id = _do_test_case(account1, account2)
        self.assertIsNotNone(doc_id)

    def test_pinterest_pinterest(self):
        account1 = {'platform': 'pinterest', 'account': pin_accounts[0]}
        account2 = {'platform': 'pinterest', 'account': pin_accounts[1]}
        doc_id = _do_test_case(account1, account2)
        self.assertIsNotNone(doc_id)

    def test_pinterest_flickr(self):
        account1 = {'platform': 'pinterest', 'account': pin_accounts[0]}
        account2 = {'platform': 'flickr', 'account': fli_accounts[0]}
        doc_id = _do_test_case(account1, account2)
        self.assertIsNotNone(doc_id)

    def test_flickr_flickr(self):
        account1 = {'platform': 'flickr', 'account': fli_accounts[0]}
        account2 = {'platform': 'flickr', 'account': fli_accounts[1]}
        doc_id = _do_test_case(account1, account2)
        self.assertIsNotNone(doc_id)


def _do_test_case(account1, account2):
    handler = SimCalculator()
    info1 = retrieve(account1, REALTIME_MODE)
    info2 = retrieve(account2, REALTIME_MODE)
    info1['platform'] = account1['platform'].lower()
    info2['platform'] = account2['platform'].lower()
    vector = handler.calc(info1, info2, enable_networking=False, mode=REALTIME_MODE)
    doc_id = handler.store_result(info1, info2, vector, DATABASE_DATA_AWAIT_FEEDBACK)
    return doc_id


if __name__ == '__main__':
    unittest.main()
