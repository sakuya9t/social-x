import unittest

from constant import REALTIME_MODE
from similarity.OverallSimilarityCalculator import OverallSimilarityCalculator


class OverallSimilarityCalculatorTests(unittest.TestCase):
    def test_calc_realtime(self):
        data = {
                  "_id": "790b0d582972385cab7d4f1b99046a5d",
                  "_rev": "3-e3940249fb6dad87fb2a67b62899fa65",
                  "platform1": "twitter",
                  "platform2": "instagram",
                  "username1": "@an_lack",
                  "username2": "Lucky lucky",
                  "vector": {
                    "username": "0.9090909090909091",
                    "profileImage": "0.5843206644058228",
                    "self_desc": "0.21212448179721832",
                    "desc_overlap_url_count": 0
                  },
                  "timestamp": 1570095218
                }
        score = OverallSimilarityCalculator().calc(data, REALTIME_MODE)
        print(score)
        self.assertTrue(0 <= score <= 1)


if __name__ == '__main__':
    unittest.main()
