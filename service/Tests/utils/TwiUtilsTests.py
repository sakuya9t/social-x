import unittest

from utils.InvalidAccountException import InvalidAccountException
from utils.TwiUtils import TwiUtilsNoLogin


class TwiUtilsTests(unittest.TestCase):
    def test_parse(self):
        u = TwiUtilsNoLogin()
        info = u.parse('enako_cos')
        u.close()
        self.assertTrue('profile' in info.keys() and 'posts_content' in info.keys())
        for item in info['posts_content']:
            self.assertTrue('text' in item.keys() and 'image' in item.keys())

    def test_parse_profile(self):
        u = TwiUtilsNoLogin()
        info = u.parse_profile('@enako_cos')
        u.close()
        print(info)

    def test_get_post_content(self):
        u = TwiUtilsNoLogin()
        url = 'https://twitter.com/enako_cos/status/1174552955409711104'
        content = u.get_post_content(url)
        self.assertTrue('text' in content.keys() and 'image' in content.keys())

    def test_parse_protect(self):
        u = TwiUtilsNoLogin()
        content = u.parse('DarkcryEwan')
        u.close()
        self.assertTrue('profile' in content.keys() and 'posts_content' in content.keys())

    def test_parse_empty(self):
        u = TwiUtilsNoLogin()
        content = u.parse('JayMains')
        u.close()
        self.assertTrue('profile' in content.keys() and 'posts_content' in content.keys())

    def test_parse_invalid_should_raise_exception(self):
        u = TwiUtilsNoLogin()
        with self.assertRaises(InvalidAccountException):
            u.parse('enako_cos334455')
        u.close()
        u = TwiUtilsNoLogin()
        with self.assertRaises(InvalidAccountException):
            u.parse('greatone9')
        u.close()


if __name__ == '__main__':
    unittest.main()
