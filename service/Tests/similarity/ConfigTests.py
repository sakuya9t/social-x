import unittest

from similarity.Config import Config


class ConfigTests(unittest.TestCase):
    def test_set_attribute(self):
        filename = '../../config/config-test.json'
        config = Config(filename)
        config.set('uclassify/apikey', 'aaabbb')


if __name__ == '__main__':
    unittest.main()
