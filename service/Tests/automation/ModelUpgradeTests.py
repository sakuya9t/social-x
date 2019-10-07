import unittest
from datetime import date
import os
import pandas as pd

from tensorflow.python.keras import Sequential

from automation.batch.ModelUpgrade import generate_model, export_model, import_model, upgrade_model_batch, import_stats
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

    def test_export_model_realtime(self):
        enable_crossfeature = True
        model = generate_model(REALTIME_MODE, cross_features=enable_crossfeature)
        export_model(model, REALTIME_MODE, enable_crossfeature)
        date_str = date.today().strftime('%y%m%d')
        jsonfile_path = MODEL_FILE_BASE_PATH + "model_realtime{}.json".format(date_str)
        h5file_path = MODEL_FILE_BASE_PATH + "model_realtime{}.h5".format(date_str)
        self.assertTrue(os.path.exists(jsonfile_path) and os.path.exists(h5file_path))

    def test_export_model_batch(self):
        enable_crossfeature = True
        model = generate_model(BATCH_MODE, cross_features=enable_crossfeature)
        export_model(model, BATCH_MODE, enable_crossfeature)
        date_str = date.today().strftime('%y%m%d')
        jsonfile_path = MODEL_FILE_BASE_PATH + "model_batch{}.json".format(date_str)
        h5file_path = MODEL_FILE_BASE_PATH + "model_batch{}.h5".format(date_str)
        self.assertTrue(os.path.exists(jsonfile_path) and os.path.exists(h5file_path))

    def test_import_model(self):
        model = import_model('model_batch191007')
        self.assertTrue(isinstance(model, Sequential))
        model = import_model('model_realtime191007')
        self.assertTrue(isinstance(model, Sequential))

    def test_batch(self):
        upgrade_model_batch()

    def test_import_stats(self):
        filename = MODEL_FILE_BASE_PATH + "stats191007.json"
        stats = import_stats(filename)
        self.assertTrue(isinstance(stats, pd.DataFrame))


if __name__ == '__main__':
    unittest.main()
