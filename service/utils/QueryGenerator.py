from utils.Couch import Couch


def generate_query(account):
    try:
        db_name = account['platform'].lower()
        username = account['account']
        query = {"username": username}
        return {"database": db_name, "selector": query}

    except Exception as e:
        print(e)


def execute_query(query):
    try:
        db = Couch("../config.json", db_name=query['database'])
        res = db.query(selector=query['selector'])
        return res

    except Exception as e:
        print(e)
