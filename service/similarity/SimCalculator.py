from similarity.Config import Config
from similarity.TextUtils import TensorSimilarity


class SimCalculator:
    def __init__(self):
        self.config = Config('algomodule.config')
        self.semantic_sim = TensorSimilarity()

    def calc(self, info1, info2):
        vector1 = self.vectorize(info1)
        vector2 = self.vectorize(info2)
        return 1

    def vectorize(self, raw_data):
        return []
