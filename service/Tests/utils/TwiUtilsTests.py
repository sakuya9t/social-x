import unittest

from utils.TwiUtils import TwiUtilsNoLogin


class TwiUtilsTests(unittest.TestCase):
    def test_parse(self):
        u = TwiUtilsNoLogin()
        info = u.parse('enako_cos')
        u.close()
        self.assertTrue('profile' in info.keys() and 'posts_content' in info.keys())
        for item in info['posts_content']:
            self.assertTrue('text' in item.keys() and 'image' in item.keys())

    def test_get_post_content(self):
        u = TwiUtilsNoLogin()
        url = 'https://twitter.com/enako_cos/status/1174552955409711104'
        content = u.get_post_content(url)
        self.assertTrue('text' in content.keys() and 'image' in content.keys())

    def test_parse_protect(self):
        u = TwiUtilsNoLogin()
        info = u.parse('YG_iKONph')
        u.close()
        print(info)


if __name__ == '__main__':
    unittest.main()
