import ast
import random
import os

from constant import CONFIG_PATH
from similarity.Config import Config

CONFIG = Config(CONFIG_PATH)
PAIRING_FILE_PATH = CONFIG.get("sampler/pairing_file")
MODE = CONFIG.get("sampler/mode")
INSTA_FOLDER = CONFIG.get("sampler/instagram_folder")
TWITTER_FOLDER = CONFIG.get("sampler/twitter_folder")


class Sampler:
    def __init__(self):
        self.items = []
        if MODE == 'file':
            with open(PAIRING_FILE_PATH, "r") as file:
                while True:
                    line = file.readline()
                    if not line:
                        break
                    self.items.append(ast.literal_eval(line))
            dictlist = [{x['instagram']: x['twitter']} for x in self.items]
            self.ins_to_twi_dict = dict(kv for d in dictlist for kv in d.items())
            dictlist = [{x['twitter']: x['instagram']} for x in self.items]
            self.twi_to_ins_dict = dict(kv for d in dictlist for kv in d.items())

    def findTwitter(self, ins_account):
        return self.ins_to_twi_dict[ins_account]

    def findInsta(self, twi_account):
        return self.twi_to_ins_dict[twi_account]

    def _findExistingItemsIndexes(self):
        candidates = []
        for i in range(len(self.items)):
            item = self.items[i]
            ins_path = INSTA_FOLDER + "{}.txt".format(item['instagram'])
            twi_path = TWITTER_FOLDER + "{}.txt".format(item['twitter'])
            if os.path.exists(ins_path) and os.path.exists(twi_path):
                candidates.append(i)
        return candidates

    def getPositiveDataset(self, sample_size):
        candidates = self._findExistingItemsIndexes()
        exist_items = [self.items[i] for i in candidates]
        if len(candidates) > sample_size:
            indexes = random.sample(range(0, len(candidates) - 1), sample_size)
            samples = [exist_items[x] for x in indexes]
            return samples
        return exist_items

    def getNegativeDataset(self, sample_size):
        candidates = self._findExistingItemsIndexes()
        pairs = [(x, self._sampleNotEqual(x, candidates)) for x in candidates]
        if len(pairs) > sample_size:
            indexes = random.sample(range(0, len(pairs) - 1), sample_size)
            pairs = [pairs[i] for i in indexes]
        res = [{'twitter': self.items[i[0]]['twitter'], 'instagram': self.items[i[1]]['instagram']} for i in pairs]
        return res

    def _sampleNotEqual(self, index, arr):
        sample = random.sample(arr, 1)
        if sample[0] == index:
            return self._sampleNotEqual(index, arr)
        return sample[0]
