from constant import BATCH_MODE
from utils import InsUtils, TwiUtils, PinterestUtils, FlickrUtils
from utils.Couch import Couch

PARSER = {'instagram': InsUtils.InsUtils,
          'twitter': TwiUtils.TwiUtils,
          'pinterest': PinterestUtils.PinterestUtils,
          'flickr': FlickrUtils.FlickrUtils}


def generate_query(account):
    try:
        db_name = account['platform'].lower()
        username = account['account']
        query = {"profile": {"username": username}}
        return {"database": db_name, "selector": query}

    except Exception as e:
        print(e)


def execute_query(query):
    try:
        db = Couch(db_name=query['database'])
        res = db.query(selector=query['selector'])
        db.close()
        return res

    except Exception as e:
        print(e)


def retrieve(account, mode):
    query = generate_query(account)
    db_result = execute_query(query)
    if not db_result:
        return parse_and_insert(account, mode)
    if mode == BATCH_MODE:
        info = db_result[0]
        if 'posts_content' not in info.keys():
            delete_if_exist(account)
            return parse_and_insert(account, mode)
    return db_result


def delete_if_exist(account):
    platform = account['platform'].lower()
    username = account['account']
    db = Couch(platform)
    db.delete({"profile": {"username": username}})
    db.close()


def parse_and_insert(account, mode):
    platform = account['platform'].lower()
    username = account['account']
    parser = factory(platform)
    parse_result = parser.parse(username) if mode == BATCH_MODE else {'profile': parser.parse_profile(username)}
    parser.close()
    db = Couch(db_name=platform)
    db.insert(parse_result)
    db.close()
    return [parse_result]


def factory(classname):
    instance = PARSER[classname]
    return instance()
