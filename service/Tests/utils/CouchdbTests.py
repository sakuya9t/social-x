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

    def test_delete(self):
        obj = {"abc": "1234", "def": "4567"}
        selector = {"abc": "1234"}
        db = Couch('test')
        db.distinct_insert(obj)
        query_result = db.query(selector)
        self.assertTrue(len(query_result) > 0)
        db.delete(selector)
        query_result = db.query(selector)
        self.assertEqual(0, len(query_result))

    def test_update(self):
        obj = {"abc": "1234", "def": {"abc": "4567"}}
        db = Couch('test')
        doc_id = db.distinct_insert(obj)
        selector = {'_id': doc_id}
        Couch('test').update(selector, 'def', {"abc": "5678"})
        res = Couch('test').query(selector)
        for item in res:
            self.assertEqual(item['def'], {"abc": "5678"})

    def test_move_doc(self):
        obj = {"i": "tomove"}
        db = Couch('test')
        doc_id = db.distinct_insert(obj)
        selector = {'_id': doc_id}
        Couch('test').move_doc(selector, 'test2')
        query_result = Couch('test2').query(obj)
        self.assertTrue(len(query_result) > 0)


if __name__ == '__main__':
    unittest.main()
