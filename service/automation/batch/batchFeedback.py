from constant import DATABASE_FEEDBACK, DATABASE_DATA_AWAIT_FEEDBACK, DATABASE_LABELED_DATA
from utils import logger
from utils.Couch import Couch


def batch_feedback():
    feedback_await_batch = Couch(DATABASE_FEEDBACK).query_all()
    for feedback in feedback_await_batch:
        apply_feedback(feedback)
        doc_id = feedback['_id']
        Couch(DATABASE_FEEDBACK).delete({'doc_id': doc_id})


def apply_feedback(item):
    doc_id = item['doc_id']
    label = item['feedback']
    selector = {'_id': doc_id}
    db_name = DATABASE_DATA_AWAIT_FEEDBACK
    stored_records = Couch(db_name).query(selector)
    if stored_records:
        logger.info('Batching doc id {} in table {}.'.format(selector['_id'], db_name))
        item = stored_records[0]
        item['vector']['label'] = label
        Couch(db_name).update(selector, 'vector', item['vector'])
        Couch(db_name).move_doc(selector, DATABASE_LABELED_DATA)
        logger.info('Batching doc id {} in table {} finished.'.format(selector['_id'], db_name))


if __name__ == '__main__':
    batch_feedback()
