from similarity.Config import Config
from similarity.ImageUtils import webimage_similarity
from similarity.TeaUtils import query_writing_style, writing_style_similarity
from similarity.TextUtils import TensorSimilarity


class SimCalculator:
    def __init__(self, driver, config):
        self.config = Config(config)
        self.semantic_sim = TensorSimilarity()
        self.driver = driver

    def calc(self, info1, info2):
        vector = self.vectorize(info1, info2)
        return 1

    def vectorize(self, info1, info2):
        result = {}
        profile1, profile2 = info1['profile'], info2['profile']
        result['profileImage'] = self.profile_img_similarity(profile1['image'], profile2['image'])

        posts1 = info1['posts_content'] if 'posts_content' in info1.keys() else []
        posts2 = info2['posts_content'] if 'posts_content' in info2.keys() else []

        result['writingStyle'] = writing_style_similarity(posts1, posts2)
        return result

    def profile_img_similarity(self, url1, url2):
        return webimage_similarity(url1, url2)['resnet18']

    def writing_style_similarity(self, posts1, posts2):
        all_posts_text = [" ".join(posts1), " ".join(posts2)]
        writing_style = [query_writing_style(x, self.driver) for x in all_posts_text]
        return writing_style_similarity(writing_style[0], writing_style[1])
