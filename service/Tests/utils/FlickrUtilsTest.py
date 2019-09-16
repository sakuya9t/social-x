import unittest

from utils.FlickrUtils import FlickrUtils


class FlickrUtilsTest(unittest.TestCase):
    def test_parse_should_no_exception(self):
        parser = FlickrUtils(showbrowser=False, driver='../../chromedriver')
        info = parser.parse('sakuranyochan')
        parser.close()
        self.assertTrue('profile' in info.keys())
        self.assertTrue('posts_content' in info.keys())
        self.assertTrue('following' in info.keys())
        self.assertTrue('groups' in info.keys())
