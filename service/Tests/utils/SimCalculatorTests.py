import unittest


from constant import BATCH_MODE
from similarity.SimCalculator import SimCalculator
from utils.QueryGenerator import retrieve


class SimCalculatorTests(unittest.TestCase):

    def test_create_calculator(self):
        calculator = SimCalculator()
        self.assertIsNotNone(calculator)

    def test_generate_vector(self):
        account1 = {'platform': 'twitter', 'account': 'tohtohchan'}
        account2 = {'platform': 'instagram', 'account': 'tohtohchan'}
        info1 = retrieve(account1, BATCH_MODE)
        info2 = retrieve(account2, BATCH_MODE)
        info1['platform'] = account1['platform'].lower()
        info2['platform'] = account2['platform'].lower()
        vector = SimCalculator().vectorize(info1, info2, BATCH_MODE)
        print(vector)
