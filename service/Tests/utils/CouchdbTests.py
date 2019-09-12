import unittest

from utils.Couch import Couch


class CouchdbTests(unittest.TestCase):
    def test_database_query(self):
        conn = Couch("../../config.json", "asdfasdf")
        conn.select_db("test")
        selector = {"abc": "def"}
        res = conn.query(selector)
        for item in res:
            self.assertEqual(item['abc'], 'def')


if __name__ == '__main__':
    unittest.main()
