import unittest

from utils.TwiUtils import TwiUtilsNoLogin


class TwiUtilsTests(unittest.TestCase):
    def test_parse(self):
        u = TwiUtilsNoLogin()
        info = u.parse('enako_cos')
        u.close()
        print(info)


if __name__ == '__main__':
    unittest.main()
