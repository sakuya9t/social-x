import ast
import json

import requests
from sklearn.metrics.pairwise import cosine_similarity

from constant import CONFIG_PATH
from similarity.Config import Config
from utils import logger


def uclassify_topics(text):
    try:
        keys = Config(CONFIG_PATH).get('uclassify/apikey')
        url = 'https://api.uclassify.com/v1/uClassify/Topics/classify'
        data = {'texts': [text]}
        for key in keys:
            header = {'Authorization': 'Token {}'.format(key), 'Content-Type': 'application/json'}
            response = requests.post(url=url, data=json.dumps(data), headers=header)
            if response.status_code == 200:
                resp_data = ast.literal_eval(response.text)[0]['classification']
                res = {x['className']: x['p'] for x in resp_data}
                return res
        raise UclassifyKeyExceedException('All uClassify keys daily usage exceed.')
    except Exception as ex:
        logger.error('Error when uClassifying text: {}'.format(ex))


def uclassify_similarity(text1, text2):
    topics1 = uclassify_topics(text1)
    topics2 = uclassify_topics(text2)
    keys = set().union(topics1, topics2)
    vec1 = [topics1.get(key, 0) for key in keys]
    vec2 = [topics2.get(key, 0) for key in keys]
    return cosine_similarity([vec1], [vec2])[0][0]


class UclassifyKeyExceedException(BaseException):
    pass
