from automation.batch.ModelUpgrade import import_model
from constant import ALGOCONFIG_PATH, BATCH_MODE, REALTIME_MODE
from similarity.Config import Config


mode_name = {BATCH_MODE: 'batch', REALTIME_MODE: 'realtime'}


class OverallSimilarityCalculator:
    def calc(self, vector1, vector2, mode):
        model_name = Config(ALGOCONFIG_PATH).get('model-name/{}'.format(mode_name[mode]))
        model = import_model(model_name)
