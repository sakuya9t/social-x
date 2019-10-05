from constant import DATABASE_FEEDBACK, DATABASE_DATA_AWAIT_FEEDBACK, DATABASE_DATA_AWAIT_BATCH, DATABASE_LABELED_DATA
from utils import logger
from utils.Couch import Couch


def batch_feedback():
    feedback_await_batch = Couch(DATABASE_FEEDBACK).query_all()
    selectors = [{'_id': x['doc_id']} for x in feedback_await_batch]
    labels = {x['doc_id']: x['feedback'] for x in feedback_await_batch}
    candidate_database_names = [DATABASE_DATA_AWAIT_FEEDBACK, DATABASE_DATA_AWAIT_BATCH]
    for selector in selectors:
        for db_name in candidate_database_names:
            stored_records = Couch(db_name).query(selector)
            if stored_records:
                logger.info('Batching doc id {} in table {}.'.format(selector['_id'], db_name))
                item = stored_records[0]
                label = labels[item['_id']]
                item['vector']['label'] = label
                Couch(DATABASE_FEEDBACK).delete({'doc_id': selector['_id']})
                Couch(db_name).update(selector, 'vector', item['vector'])
                Couch(db_name).move_doc(selector, DATABASE_LABELED_DATA)
                logger.info('Batching doc id {} in table {} finished.'.format(selector['_id'], db_name))


if __name__ == '__main__':
    batch_feedback()
