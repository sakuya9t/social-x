import calendar
import time

from constant import CONFIG_PATH, REALTIME_MODE, ALGOCONFIG_PATH, DATABASE_LABELED_DATA, DATABASE_DATA_AWAIT_FEEDBACK
from similarity.Config import Config
from similarity.ImageUtils import webimage_similarity
from similarity.TeaUtils import query_writing_style, writing_style_similarity
from similarity.TextUtils import TensorSimilarity, singleword_similarity, desc_overlap_url
from similarity.UclassifyUtils import uclassify_similarity
from utils import logger
from utils.Couch import Couch, _convert_float, _restore_float

column_names = {
    'score': 'Overall Similarity',
    'username': 'User Name',
    'profileImage': 'Profile Image',
    'self_desc': 'Text in Self Description',
    'desc_overlap_url_count': 'URL in Self Description',
    'readability': 'Writing Style (Readability)',
    'tea': 'Writing Style (Tea)',
    'post_text': 'Text in Posts',
    'uclassify': 'UClassify Similarity'
}


class SimCalculator:
    def __init__(self):
        self.config = Config(CONFIG_PATH)
        self.semantic_sim = TensorSimilarity()

    @staticmethod
    # store result will run right after calc function.
    def store_result(info1, info2, vector, database):
        database = Couch(database)
        timestamp = calendar.timegm(time.gmtime())
        # todo: add overall similarity calculation (only) here.
        doc = {'platform1': info1['platform'], 'platform2': info2['platform'],
               'username1': info1['profile']['username'], 'username2': info2['profile']['username'],
               'vector': vector, 'timestamp': timestamp}
        logger.info('Storing result: {}'.format(doc))
        doc_id = database.distinct_insert(_convert_float(doc))
        database.close()
        return doc_id

    @staticmethod
    def fetch_vector(info1, info2, database):
        selector = {'platform1': info1['platform'], 'platform2': info2['platform'],
                    'username1': info1['profile']['username'], 'username2': info2['profile']['username']}
        database = Couch(database)
        query_res = database.query_latest_change(selector)
        return [_restore_float(x) for x in query_res]

    def calc(self, info1, info2, enable_networking, mode):
        if mode == REALTIME_MODE:
            existing_value = query_existing_similarity_in_db(_info_to_query(info1), _info_to_query(info2))
            if len(existing_value) > 0:
                logger.info('Similarity score already exist, return in REAL TIME MODE....')
                return existing_value[0]
        vector = self.__vectorize(info1, info2, mode)
        if enable_networking:
            vector['network'] = network_sim(info1, info2)
        return vector

    def __vectorize(self, info1, info2, mode):
        # todo: handle modes.
        result = {}
        profile1, profile2 = info1['profile'], info2['profile']
        logger.info('Evaluating usename...')
        result['username'] = singleword_similarity(profile1, profile2)
        logger.info('Evaluating profile image...')
        result['profileImage'] = profile_img_sim(profile1['image'], profile2['image'])
        logger.info('Evaluating self description text...')
        result['self_desc'] = self.semantic_sim.similarity(profile1.get('description', ''),
                                                           profile2.get('description', ''))

        logger.info('Evaluating self description url...')
        result['desc_overlap_url_count'] = desc_overlap_url(
            {'platform': info1['platform'], 'username': profile1['username'], 'desc': profile1.get('description', '')},
            {'platform': info2['platform'], 'username': profile2['username'], 'desc': profile2.get('description', '')})

        posts1 = info1['posts_content'] if 'posts_content' in info1.keys() else []
        posts2 = info2['posts_content'] if 'posts_content' in info2.keys() else []

        if mode == REALTIME_MODE and len(posts1) == 0 and len(posts2) == 0:
            return result

        logger.info('Evaluating writing style...')
        result['writing_style'] = writing_style_sim(posts1, posts2)
        logger.info('Evaluating post similarity...')

        max_post_enabled = bool(Config(ALGOCONFIG_PATH).get('max-post-similarity-enabled'))
        result['post_text'] = self.max_post_sim(posts1, posts2) if max_post_enabled else self.overall_post_sim(posts1,
                                                                                                               posts2)

        logger.info('Evaluating uClassify topical similarity...')
        result['uclassify'] = uclassify_similarity(" ".join(_get_post_text(posts1)), " ".join(_get_post_text(posts2)))

        logger.info('Calculation finished.')
        return result

    def overall_post_sim(self, posts1, posts2):
        posts1 = _get_post_text(posts1)
        posts2 = _get_post_text(posts2)
        sim = self.semantic_sim.similarity(' '.join(posts1), ' '.join(posts2))
        return sim

    def max_post_sim(self, posts1, posts2):
        posts1 = _get_post_text(posts1)
        posts2 = _get_post_text(posts2)
        sim = 0
        for p1 in posts1:
            for p2 in posts2:
                sim = max(sim, self.semantic_sim.similarity(p1, p2))
        return sim


def profile_img_sim(url1, url2):
    return webimage_similarity(url1, url2)['resnet18'].item()


def writing_style_sim(posts1, posts2):
    posts1 = _get_post_text(posts1)
    posts2 = _get_post_text(posts2)
    all_posts_text = [" ".join(posts1), " ".join(posts2)]
    writing_style = [query_writing_style(x) for x in all_posts_text]  # todo: handle timeout
    return writing_style_similarity(writing_style[0], writing_style[1])


def network_sim(info1, info2):
    return 0.0


def _get_post_text(posts):
    if len(posts) > 0 and not isinstance(posts[0], str):
        posts = [x['text'] for x in posts]
    return posts


def _info_to_query(info):
    return {'platform': info['platform'], 'account': info['profile']['username']}


def query_existing_similarity_in_db(account1, account2):
    database_order = [DATABASE_LABELED_DATA, DATABASE_DATA_AWAIT_FEEDBACK]
    account1 = __format_account_query(account1)
    account2 = __format_account_query(account2)
    selectors = [{'platform1': account1['platform'], 'platform2': account2['platform'],
                  'username1': account1['account'], 'username2': account2['account']},
                 {'platform1': account2['platform'], 'platform2': account1['platform'],
                  'username1': account2['account'], 'username2': account1['account']}]
    for db_name in database_order:
        for selector in selectors:
            database = Couch(db_name)
            query_res = database.query_latest_change(selector)
            if len(query_res) > 0:
                return [_restore_float(x) for x in query_res]
    return []


def __format_account_query(query):
    platform = query['platform']
    username = query['account']
    if platform.lower() == 'twitter':
        if username[0] != '@':
            username = '@' + username
        query['account'] = username
    return query
