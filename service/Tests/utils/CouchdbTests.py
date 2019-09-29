import unittest

import json

from utils.Couch import Couch, _convert_float, _restore_float


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

    def test_query_latest(self):
        conn = Couch("test")
        selector = {"abc": "def"}
        res = conn.query_latest_change(selector)
        conn.close()
        self.assertEqual(1, len(res))

    def test_convert_float_object(self):
        obj = {'platform1': 'twitter', 'platform2': 'instagram',
               'username1': '1angharad_rees', 'username2': 'kaligraphicprint',
               'vector': {'username': 0.25, 'profileImage': 0.45704108,
                          'self_desc': 0.4699023962020874, 'desc_overlap_url_count': 0,
                          'writing_style': {'a': 0.5, 'b': 0.4}}}
        obj = _convert_float(obj)
        print(obj)
        s = json.dumps(obj)
        self.assertNotEqual(len(s), 0)

    def test_restore_float_object(self):
        obj = {"platform1": "twitter", "platform2": "instagram", "username1": "1angharad_rees", "username2": "kaligraphicprint", "vector": {"username": "0.25", "profileImage": "0.45704108", "self_desc": "0.4699023962020874", "desc_overlap_url_count": 0, "writing_style": {"a": "0.5", "b": "0.4"}}}
        res_obj = _convert_float(_restore_float(obj))
        self.assertEqual(obj, res_obj)


if __name__ == '__main__':
    unittest.main()
