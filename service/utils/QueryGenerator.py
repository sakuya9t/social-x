from constant import BATCH_MODE
from utils import InsUtils, TwiUtils, PinterestUtils, FlickrUtils, logger
from utils.Couch import Couch

PARSER = {
          'instagram': InsUtils.InsUtilsNoLogin,
          'twitter': TwiUtils.TwiUtilsNoLogin,
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
        if len(res) > 1:
            res = db.query_latest_change(query['selector'])
        db.close()
        return res

    except Exception as e:
        print(e)


def retrieve(account, mode):
    """
    :param account: {'platform': xxx, 'account': yyy}
    :param mode: BATCH_MODE || REALTIME_MODE
    :return: JSON formatted account
    """
    query = generate_query(account)
    db_result = execute_query(query)
    if not db_result:
        return parse_and_insert(account, mode)[0]
    if mode == BATCH_MODE:
        info = db_result[0]
        if 'posts_content' not in info.keys():
            delete_if_exist(account)
            return parse_and_insert(account, mode)[0]
    return db_result[0]


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
    parse_result = parser.parse(username) if mode == BATCH_MODE else {'profile': parser.parse_profile(username), 'posts_content': []}
    logger.info(parse_result)
    parser.close()
    db = Couch(db_name=platform)
    db.insert(parse_result)
    db.close()
    return [parse_result]


def factory(classname):
    instance = PARSER[classname]
    return instance()
