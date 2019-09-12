from similarity.Config import Config
from similarity.ImageUtils import webimage_similarity
from similarity.TextUtils import TensorSimilarity


class SimCalculator:
    def __init__(self):
        self.config = Config('algomodule.config')
        self.semantic_sim = TensorSimilarity()

    def calc(self, info1, info2):
        vector = self.vectorize(info1, info2)
        return 1

    def vectorize(self, info1, info2):
        result = {}
        profile1, profile2 = info1['profile'], info2['profile']
        result['profileImage'] = self.profile_img_similarity(profile1['image'], profile2['image'])
        if 'posts_content' in info1.keys():
            posts = info1['posts_content']
        else:
            posts = []
        return []

    def profile_img_similarity(self, url1, url2):
        return webimage_similarity(url1, url2)['resnet18']
