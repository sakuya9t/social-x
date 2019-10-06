import unittest

from automation.batch.ModelUPgrade import get_model_from_database
from constant import BATCH_MODE, REALTIME_MODE


class ModelUpgradeTests(unittest.TestCase):
    def test_batch_no_crossfeature(self):
        model = get_model_from_database(BATCH_MODE, cross_features=False)

    def test_batch_with_crossfeature(self):
        model = get_model_from_database(BATCH_MODE, cross_features=True)

    def test_realtime_no_crossfeature(self):
        model = get_model_from_database(REALTIME_MODE, cross_features=False)

    def test_realtime_with_crossfeature(self):
        model = get_model_from_database(REALTIME_MODE, cross_features=True)


if __name__ == '__main__':
    unittest.main()
