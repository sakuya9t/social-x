from similarity import TextUtils
from similarity.Config import Config


class SimCalculator:
    def __init__(self):
        self.config = Config('algomodule.config')
        TextUtils.initialize()

    def calc(self, info1, info2):
        return 1
