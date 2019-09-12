import unittest

from utils.QueryGenerator import generate_query


class QueryGeneratorTests(unittest.TestCase):
    def test_generate_query(self):
        account = {'platform': 'Instagram', 'account': 'beckaa_lee'}
        query = generate_query(account)
        self.assertEqual({"database": 'instagram', "selector": {"username": 'beckaa_lee'}}, query)


if __name__ == '__main__':
    unittest.main()
