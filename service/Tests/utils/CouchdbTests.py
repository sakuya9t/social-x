import unittest

from utils.Couch import Couch


class CouchdbTests(unittest.TestCase):
    def test_database_insert_and_query(self):
        conn = Couch("test")
        test_doc = {"abc": "def"}
        conn.insert(test_doc)
        selector = {"abc": "def"}
        res = conn.query(selector)
        for item in res:
            self.assertEqual(item['abc'], 'def')

    def test_distinct_insert(self):
        conn = Couch("test")
        test_doc = {"adsf": "fdsa"}
        for i in range(3):
            conn.distinct_insert(test_doc)
        query_result = conn.query(test_doc)
        self.assertEqual(1, len(query_result))


if __name__ == '__main__':
    unittest.main()
