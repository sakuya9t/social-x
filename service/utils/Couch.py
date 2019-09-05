from cloudant.client import CouchDB
from cloudant.database import CloudantDatabase
from cloudant.document import Document
from cloudant.database import CouchDatabase

from similarity.Config import Config


class Couch:
    db = None
    c_db = None
    couch_db = None

    # usage: database = Couch(db_name)
    # fields: db_name -> str
    def __init__(self, config_path, db_name):
        server_config = Config(config_path).get('couchdb')
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

    # insert operation of the database;
    # usage: database.insert(doc);
    # fields: doc -> Dictionary
    def insert(self, doc):
        document = self.db.create_document(doc)
        if document.exists():
            return document['_id']

    # update operation of the database;
    # usage: database.update(field, old_value, new_value)
    # fields: field -> str; value -> str; new_value -> str
    def update(self, field, value, new_value):
        selector = {field: value}
        q_res = self.c_db.get_query_result(selector)
        for document in q_res:
            id = document['_id']
            doc = Document(self.db, id)
            doc.update_field(
                action=doc.field_set,
                field=field,
                value=new_value
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


if __name__ == "__main__":
    conn = Couch("../config.json", "asdfasdf")
    conn.select_db("test")
    test_doc = {"abc": "def"}
    print(conn.insert(test_doc))
    print(conn.query({"abc": "def"}))
