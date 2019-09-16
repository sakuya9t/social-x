import unittest

from utils.InsUtils import InsUtilsNoLogin


class InsUtilsTests(unittest.TestCase):
    def test_parse_no_login_post_content(self):
        u = InsUtilsNoLogin(displayed=False)
        page_content = u.get_post_content("https://www.instagram.com/p/BKj_8N2A96m/")
        self.assertTrue('text' in page_content.keys() and 'image' in page_content.keys())
