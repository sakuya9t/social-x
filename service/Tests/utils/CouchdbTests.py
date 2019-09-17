import unittest

from utils.Couch import Couch


class CouchdbTests(unittest.TestCase):
    def test_database_query(self):
        conn = Couch("asdfasdf")
        conn.select_db("test")
        test_doc = {"abc": "def"}
        conn.insert(test_doc)
        selector = {"abc": "def"}
        res = conn.query(selector)
        for item in res:
            self.assertEqual(item['abc'], 'def')


if __name__ == '__main__':
    unittest.main()
