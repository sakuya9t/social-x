import ast
import os

from utils import logger
from utils.Couch import Couch


def import_file_to_db(path, db):
    with open(path, 'r') as file:
        content = file.read()
        doc = ast.literal_eval(content)
        db.distinct_insert(doc)


def import_directory_to_db(path, db_name):
    db = Couch(db_name)
    files = os.listdir(path)
    cnt = 0
    for filename in files:
        if cnt % 100 == 0:
            print('Processing {} of {} records.'.format(cnt, len(files)))
        cnt += 1
        import_file_to_db(path + "/" + filename, db)
    logger.info('{} records inserted.'.format(len(files)))
    db.close()


if __name__ == '__main__':
    import_directory_to_db("/data/dev/insdata", "instagram")
    import_directory_to_db("/data/dev/twidata", "twitter")
