import calendar
import time

from cloudant.client import CouchDB
from cloudant.database import CloudantDatabase
from cloudant.database import CouchDatabase
from cloudant.document import Document

from constant import CONFIG_PATH
from similarity.Config import Config


class Couch:
    db = None
    c_db = None
    couch_db = None

    # usage: database = Couch(db_name)
    # fields: db_name -> str
    def __init__(self, db_name):
        server_config = Config(CONFIG_PATH).get('couchdb')
        self.client = CouchDB(server_config['username'], server_config['password'], url=server_config['server_addr'],
                              connect=True, auto_renew=True)
        self.select_db(db_name)

    # Get one database selected; if the database doesn't exist, create it.
    # usage: database.select_db(db_name);
    # fields: db_name -> str
    def select_db(self, db_name):
        self.couch_db = CouchDatabase(self.client, db_name)
        if not self.couch_db.exists():
            self.couch_db.create()
        self.db = self.client[db_name]
        self.c_db = CloudantDatabase(self.client, db_name)

    # usage: database.close()
    # Database should be closed when finish using
    def close(self):
        self.client.disconnect()

    # Get count of documents in current database;
    # usage database.count();
    def count(self):
        return self.couch_db.doc_count()

    # Get everything from the database;
    # usage: database.query_all();
    # note: after query_all, iterate the returned item to get every document
    def query_all(self):
        qlist = []
        for doc in self.db:
            qlist.append(doc)
        return qlist

    # Select something from the database;
    # usage: database.query(selector);
    # fields: selector -> Dictionary
    # note: after query, iterate the returned item to get every document
    def query(self, selector):
        qlist = []
        result = self.c_db.get_query_result(selector)
        for doc in result:
            qlist.append(doc)
        return qlist

    def query_multiple(self, selectors):
        qlist = []
        for selector in selectors:
            qlist += self.query(selector)
        return qlist

    # insert operation of the database;
    # usage: database.insert(doc);
    # fields: doc -> Dictionary
    def insert(self, doc):
        doc['timestamp'] = _timestamp()
        document = self.db.create_document(doc)
        if document.exists():
            return document['_id']

    def distinct_insert(self, doc):
        query_res = self.query(doc)
        if len(query_res) == 0:
            return self.insert(doc)
        return query_res[0]['_id']

    # update operation of the database;
    # usage: database.update(field, old_value, new_value)
    # fields: field -> str; value -> str; new_value -> str
    def update(self, selector, field, new_value):
        q_res = self.c_db.get_query_result(selector)
        for document in q_res:
            doc_id = document['_id']
            doc = Document(self.db, doc_id)
            doc.update_field(
                action=doc.field_set,
                field=field,
                value=new_value
            )
            doc.update_field(
                action=doc.field_set,
                field='timestamp',
                value=_timestamp()
            )

    # delete operation of the database;
    # usage: database.delete(selector)
    # fields: selector -> Dictionary
    def delete(self, selector):
        q_res = self.c_db.get_query_result(selector)
        for document in q_res:
            id = document['_id']
            rev = document['_rev']
            doc = Document(self.db, id)
            doc['_rev'] = rev
            doc.delete()

    def move_doc(self, selector, target):
        """
        Move documents from current database to target database.
        :param selector: dictionary
        :param target: string, db name
        :return:
        """
        documents = self.query(selector)
        for doc in documents:
            del doc['_id']
            del doc['_rev']
            Couch(target).distinct_insert(doc)
        self.delete(selector)

    def query_latest_change(self, selector):
        """
        Query latest item sorted by timestamp. Returns only timestamp in documents.
        :param selector: dictionary
        :return: a list that contains 1 or 0 docs
        """
        q_res = self.query(selector)
        q_res = list(filter(lambda x: 'timestamp' in x.keys(), q_res))
        res = sorted(q_res, key=lambda x: x['timestamp'])
        return res[-1:]


def _convert_float(obj):
    for key, value in obj.items():
        if isinstance(value, float):
            obj[key] = str(value)
        elif isinstance(value, dict):
            obj[key] = _convert_float(value)
    return obj


def _restore_float(obj):
    for key, value in obj.items():
        if isinstance(value, dict):
            obj[key] = _restore_float(value)
        else:
            try:
                obj[key] = float(value)
            except ValueError:
                pass
    return obj


def _timestamp():
    return calendar.timegm(time.gmtime())
