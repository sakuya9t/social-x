import unittest

from utils.InvalidAccountException import InvalidAccountException
from utils.InsUtils import InsUtilsNoLogin


class InsUtilsTests(unittest.TestCase):
    def test_parse_no_login_post_content(self):
        u = InsUtilsNoLogin(displayed=False)
        page_content = u.get_post_content("https://www.instagram.com/p/BKj_8N2A96m/")
        u.close()
        self.assertTrue('text' in page_content.keys() and 'image' in page_content.keys())

    def test_invalid_account_should_raise_exception(self):
        u = InsUtilsNoLogin(displayed=False)
        with self.assertRaises(InvalidAccountException):
            u.parse('asdfsadg')
        u.close()


if __name__ == '__main__':
    unittest.main()
