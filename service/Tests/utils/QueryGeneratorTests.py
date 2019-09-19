import unittest

from utils import InsUtils, TwiUtils, PinterestUtils, FlickrUtils
from utils.Couch import Couch
from utils.QueryGenerator import generate_query, factory, retrieve
from constant import REALTIME_MODE, BATCH_MODE


class QueryGeneratorTests(unittest.TestCase):
    def test_generate_query(self):
        account = {'platform': 'Instagram', 'account': 'beckaa_lee'}
        query = generate_query(account)
        self.assertEqual({"database": 'instagram', "selector": {"username": 'beckaa_lee'}}, query)

    def test_factory_insta(self):
        instance = factory('instagram')
        instance.close()
        self.assertTrue(isinstance(instance, InsUtils.InsUtils))

    def test_factory_twi(self):
        instance = factory('twitter')
        instance.close()
        self.assertTrue(isinstance(instance, TwiUtils.TwiUtils))

    def test_factory_pinterest(self):
        instance = factory('pinterest')
        instance.close()
        self.assertTrue(isinstance(instance, PinterestUtils.PinterestUtils))

    def test_factory_flickr(self):
        instance = factory('flickr')
        instance.close()
        self.assertTrue(isinstance(instance, FlickrUtils.FlickrUtils))

    def test_retrieve_flickr_realtime_in_db(self):
        account = {'platform': 'Flickr', 'account': 'sakuranyochan'}
        retrieve(account, REALTIME_MODE)
        db = Couch('flickr')
        query_result = db.query({'profile': {'username': 'sakuranyochan'}})
        db.close()
        self.assertTrue(len(query_result) > 0)
        query_result = retrieve(account, REALTIME_MODE)
        for item in query_result:
            self.assertTrue('profile' in item.keys() and item['profile']['username'] == 'sakuranyochan')

    def test_retrieve_flickr_batch_in_db(self):
        account = {'platform': 'Flickr', 'account': 'sakuranyochan'}
        query_result = retrieve(account, BATCH_MODE)
        for item in query_result:
            self.assertTrue('profile' in item.keys() and item['profile']['username'] == 'sakuranyochan')
            self.assertTrue('posts_content' in item.keys())

    def test_retrieve_flickr_realtime_not_in_db(self):
        selector = {'profile': {'username': 'sakuranyochan'}}
        db = Couch('flickr')
        db.delete(selector)
        db.close()
        account = {'platform': 'Flickr', 'account': 'sakuranyochan'}
        retrieve(account, REALTIME_MODE)
        db = Couch('flickr')
        query_result = db.query({'profile': {'username': 'sakuranyochan'}})
        db.close()
        for item in query_result:
            self.assertTrue('profile' in item.keys() and item['profile']['username'] == 'sakuranyochan')


if __name__ == '__main__':
    unittest.main()
