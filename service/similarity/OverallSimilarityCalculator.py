from automation.batch.ModelUpgrade import import_model, import_stats, generate_dataset, norm, generate_feature_vectors
from constant import ALGOCONFIG_PATH, BATCH_MODE, REALTIME_MODE, MODEL_FILE_BASE_PATH
from similarity.Config import Config

mode_name = {BATCH_MODE: 'batch', REALTIME_MODE: 'realtime'}
enable_crossfeature = Config(ALGOCONFIG_PATH).get('enable-cross-feature')


class OverallSimilarityCalculator:
    def _calc(self, data, mode):
        model_name = Config(ALGOCONFIG_PATH).get('model-name/{}'.format(mode_name[mode]))
        stat_path = MODEL_FILE_BASE_PATH + Config(ALGOCONFIG_PATH).get(
            'model-name/train-stats/{}'.format(mode_name[mode]))
        model = import_model(model_name)
        train_stats = import_stats(stat_path)
        data['vector']['label'] = -1
        feature_vectors = generate_feature_vectors(items=[data], mode=mode, cross_features=enable_crossfeature)
        test_set = generate_dataset(data_list=feature_vectors, mode=mode,
                                    cross_features=enable_crossfeature)
        test_set.pop('label')
        normed_test_data = norm(test_set, train_stats)
        test_predictions = model.predict(normed_test_data).flatten()
        return _limit_range(test_predictions[0], lower=0, upper=1)

    def calc(self, data):
        if has_full_property(data):
            return self._calc(data, BATCH_MODE)
        return self._calc(data, REALTIME_MODE)


def has_full_property(data):
    vector = data['vector']
    return 'post_text' in vector.keys()


def _limit_range(value, lower, upper):
    return max(lower, min(upper, value))
