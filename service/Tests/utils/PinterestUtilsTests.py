import unittest

from utils.PinterestUtils import PinterestUtils


class PinterestUtilsTest(unittest.TestCase):
    def test_parse_profile(self):
        parser = PinterestUtils()
        info = parser.parse_profile('deathjazz69')
        print(info)
        parser.close()
        for key in ['username', 'name', 'description', 'image']:
            self.assertTrue(key in info.keys())


if __name__ == '__main__':
    unittest.main()
