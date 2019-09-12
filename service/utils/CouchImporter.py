import os
import json
from utils.Couch import Couch


def import_file_to_db(path, db):
    with open(path, 'r') as file:
        content = file.read()
        doc = json.loads(content)
        doc_id = db.insert(doc)


def import_directory_to_db(path, db_name):
    db = Couch("../config.json", db_name)
    for filename in os.listdir(path):
        import_file_to_db(path + "/" +filename, db)


if __name__ == '__main__':
    import_directory_to_db("/data/dev/insdata", "asdf")
