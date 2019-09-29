import unittest

from utils.InvalidAccountException import InvalidAccountException
from utils.InsUtils import InsUtilsNoLogin, is_valid_instagram_data


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

    def test_isvalid_content_not_exist(self):
        content = {'profile': {'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/7dd8e74bdf967057a131a06afacf16b1/5DFA7AD1/t51.2885-19/11311564_1626602367578081_1750564427_a.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'username': 'thedunkstar', 'status': 'PRIVATE', 'description': 'Duncan Reddell;;'}}
        self.assertTrue(is_valid_instagram_data(content))

    def test_isvalid_profile_not_exist_should_be_invalid(self):
        content = {'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/7dd8e74bdf967057a131a06afacf16b1/5DFA7AD1/t51.2885-19/11311564_1626602367578081_1750564427_a.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'username': 'thedunkstar', 'status': 'PRIVATE', 'description': 'Duncan Reddell;;'}
        self.assertFalse(is_valid_instagram_data(content))

    def test_parse_account(self):
        u = InsUtilsNoLogin(displayed=False)
        info = u.parse('enakorin')
        self.assertTrue('profile' in info.keys() and 'posts_content' in info.keys())
        for item in info['posts_content']:
            self.assertTrue('text' in item.keys() and 'image' in item.keys())


if __name__ == '__main__':
    unittest.main()
