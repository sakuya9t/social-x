from similarity.Config import Config
from similarity.ImageUtils import webimage_similarity
from similarity.TeaUtils import query_writing_style, writing_style_similarity
from similarity.TextUtils import TensorSimilarity, singleword_similarity, desc_overlap_url
from constant import CONFIG_PATH, REALTIME_MODE, BATCH_MODE, DATABASE_SIMILARITY_VECTOR
from utils import logger
from utils.Couch import Couch


class SimCalculator:
    def __init__(self):
        self.config = Config(CONFIG_PATH)
        self.semantic_sim = TensorSimilarity()

    def store_result(self, vector):
        database = Couch(DATABASE_SIMILARITY_VECTOR)
        database.distinct_insert(vector)

    def calc(self, info1, info2, enable_networking, mode):
        vector = self.vectorize(info1, info2, mode)
        if enable_networking:
            vector['network'] = network_sim(info1, info2)
        return vector

    def vectorize(self, info1, info2, mode):
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

        logger.info('Evaluating writing style...')
        result['writing_style'] = writing_style_sim(posts1, posts2)
        logger.info('Evaluating post similarity...')
        result['post_text'] = overall_post_sim(posts1, posts2) if mode == REALTIME_MODE else max_post_sim(posts1,
                                                                                                          posts2)
        return result


def profile_img_sim(url1, url2):
    return webimage_similarity(url1, url2)['resnet18']


def writing_style_sim(posts1, posts2):
    if len(posts1) > 0 and not isinstance(posts1[0], str):
        posts1 = [x['text'] for x in posts1]
    if len(posts2) > 0 and not isinstance(posts2[0], str):
        posts2 = [x['text'] for x in posts2]
    all_posts_text = [" ".join(posts1), " ".join(posts2)]
    writing_style = [query_writing_style(x) for x in all_posts_text]
    return writing_style_similarity(writing_style[0], writing_style[1])


def network_sim(info1, info2):
    return 0.0


def overall_post_sim(posts1, posts2):
    return 0.0


def max_post_sim(posts1, posts2):
    return 0.0
