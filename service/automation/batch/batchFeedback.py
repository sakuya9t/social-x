from constant import DATABASE_FEEDBACK, DATABASE_DATA_AWAIT_FEEDBACK, DATABASE_DATA_AWAIT_BATCH
from utils.Couch import Couch

feedbacks_await_batch = Couch(DATABASE_FEEDBACK).query_all()
selectors = [{'_id': x['doc_id']} for x in feedbacks_await_batch]
candidate_database_names = [DATABASE_DATA_AWAIT_FEEDBACK, DATABASE_DATA_AWAIT_BATCH]
for db_name in candidate_database_names:
    curr_res = Couch(db_name).query_multiple(selectors)
    print(curr_res)
print(selectors)

