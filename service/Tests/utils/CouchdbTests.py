import unittest

from utils.Couch import Couch


class CouchdbTests(unittest.TestCase):
    def test_database_insert_and_query(self):
        conn = Couch("test")
        test_doc = {"abc": "def"}
        conn.insert(test_doc)
        selector = {"abc": "def"}
        res = conn.query(selector)
        conn.close()
        for item in res:
            self.assertEqual(item['abc'], 'def')

    def test_database_insert_and_partial_query(self):
        conn = Couch("test")
        test_doc = {"adsf": {"bbb": "fdsa", "aand": "ssss"}}
        conn.insert(test_doc)
        selector = {"asdf": {"bbb": "fdsa"}}
        res = conn.query(selector)
        conn.close()
        for item in res:
            self.assertEqual(item, test_doc)

    def test_distinct_insert(self):
        conn = Couch("test")
        test_doc = {"adsf": "fdsa"}
        for i in range(3):
            conn.distinct_insert(test_doc)
        query_result = conn.query(test_doc)
        conn.close()
        self.assertEqual(1, len(query_result))

    def test_distinct_insert2(self):
        conn = Couch("test")
        test_doc = {"adsf": {"bbb": "fdsa", "aand": "ssss"}}
        for i in range(3):
            conn.distinct_insert(test_doc)
        query_result = conn.query(test_doc)
        conn.close()
        self.assertEqual(1, len(query_result))


if __name__ == '__main__':
    unittest.main()
