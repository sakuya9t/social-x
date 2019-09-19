import unittest

from utils import InsUtils, TwiUtils, PinterestUtils, FlickrUtils
from utils.QueryGenerator import generate_query, factory


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


if __name__ == '__main__':
    unittest.main()
