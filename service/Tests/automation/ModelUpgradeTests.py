import unittest
from datetime import date
import os

from tensorflow.python.keras import Sequential

from automation.batch.ModelUPgrade import generate_model, export_model, import_model
from constant import BATCH_MODE, REALTIME_MODE, MODEL_FILE_BASE_PATH


class ModelUpgradeTests(unittest.TestCase):
    def test_batch_no_crossfeature(self):
        model = generate_model(BATCH_MODE, cross_features=False)

    def test_batch_with_crossfeature(self):
        model = generate_model(BATCH_MODE, cross_features=True)

    def test_realtime_no_crossfeature(self):
        model = generate_model(REALTIME_MODE, cross_features=False)

    def test_realtime_with_crossfeature(self):
        model = generate_model(REALTIME_MODE, cross_features=True)

    def test_export_model(self):
        model = generate_model(REALTIME_MODE, cross_features=True)
        export_model(model)
        date_str = date.today().strftime('%y%m%d')
        jsonfile_path = MODEL_FILE_BASE_PATH + "model{}.json".format(date_str)
        h5file_path = MODEL_FILE_BASE_PATH + "model{}.h5".format(date_str)
        self.assertTrue(os.path.exists(jsonfile_path) and os.path.exists(h5file_path))

    def test_import_model(self):
        model = import_model('model191006')
        self.assertTrue(isinstance(model, Sequential))


if __name__ == '__main__':
    unittest.main()
