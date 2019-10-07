import unittest

from constant import REALTIME_MODE, BATCH_MODE
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

    def test_calc_batch(self):
        data = {
            "_id": "5475aa38048c626ea3f4b0cc530598f8",
            "_rev": "1-320b9ced40c4e1ec4befdc5f71a1607a",
            "platform1": "twitter",
            "platform2": "instagram",
            "username1": "@kpets17",
            "username2": "kpet17isu",
            "vector": {
                "username": "0.5555555555555556",
                "profileImage": "0.5929020643234253",
                "self_desc": "0.4109365940093994",
                "desc_overlap_url_count": 0,
                "writing_style": {
                    "readability": "-0.23669112013670138"
                },
                "post_text": "0.521873950958252",
                "uclassify": "0.9459866289693667",
            }
        }
        score = OverallSimilarityCalculator().calc(data, BATCH_MODE)
        print(score)
        self.assertTrue(0 <= score <= 1)


if __name__ == '__main__':
    unittest.main()
