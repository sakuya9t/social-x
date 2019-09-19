from utils import InsUtils, TwiUtils, PinterestUtils, FlickrUtils
from utils.Couch import Couch
from constant import REALTIME_MODE

PARSER = {'instagram': InsUtils.InsUtils,
          'twitter': TwiUtils.TwiUtils,
          'pinterest': PinterestUtils.PinterestUtils,
          'flickr': FlickrUtils.FlickrUtils}


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
        db = Couch(db_name=query['database'])
        res = db.query(selector=query['selector'])
        return res

    except Exception as e:
        print(e)


def retrieve(account, mode):
    query = generate_query(account)
    db_result = execute_query(query)
    if not db_result:
        platform = account['platform'].lower()
        username = account['account']
        parser = factory(platform)
        parse_result = parser.parse(username) if mode == REALTIME_MODE else {'profile': parser.parse_profile(username)}
        Couch(db_name=platform).insert(parse_result)
        return parse_result
    return db_result


def factory(classname):
    instance = PARSER[classname]
    return instance()
