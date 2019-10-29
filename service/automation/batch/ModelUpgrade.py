from datetime import date

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.python.keras.models import model_from_json

from similarity.Config import Config
from utils import logger
from tensorflow import keras
from constant import REALTIME_MODE, BATCH_MODE, DATABASE_LABELED_DATA, MODEL_FILE_BASE_PATH, ALGOCONFIG_PATH
from utils.Couch import Couch

"""
Auto model updating module.


Dependency:
DATABASE_LABELED_DATA database


Description:
This module will update the model file (/model) and will update the model path in the algomodule config file.
When running, it gets training data from the DATABASE_LABELED_DATA database.

Will generate batch and realtime two models. To turn on/off cross-feature, change the option in algomodule config.

We should run this module once a day to guarantee we are utilizing the latest data.
"""

EPOCHS = 1000
FEATURE_COUNT_REALTIME = 3
FEATURE_COUNT_BATCH = 6


def norm(x, train_stats):
    return (x - train_stats['mean']) / train_stats['std']


def build_model(train_dataset):
    _model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    _model.compile(loss='mse',
                   optimizer=optimizer,
                   metrics=['mae', 'mse'])
    return _model


def __unpack_feature_dict(item):
    return [list([float(a) for a in x.values()]) if isinstance(x, dict) else [float(x)] for x in item['vector'].values()]


def generate_feature_vectors(items, mode, cross_features):
    l = [__unpack_feature_dict(item) for item in items]
    if mode == REALTIME_MODE:
        l = [x[0:3] + x[-1:] for x in l]
    else:
        l = [x[0:3] + x[4:] for x in l]
        l = list(filter(lambda x: len(x) == 7, l))

    if cross_features:
        if mode == REALTIME_MODE:
            l = [np.append(np.array(item[:-1]).dot(np.array(item[:-1]).reshape((1, FEATURE_COUNT_REALTIME))).flatten(),
                           item[-1]) for item in l]
        else:
            l = [np.append(np.array(item[:-1]).dot(np.array(item[:-1]).reshape((1, FEATURE_COUNT_BATCH))).flatten(),
                           item[-1]) for item in l]
    else:
        l = [np.array(x).flatten() for x in l]
    return l


def __get_column_names(mode, cross_features):
    if mode == REALTIME_MODE:
        if cross_features:
            column_names = ['feature{}'.format(i) for i in range(0, 9)]
            column_names.append('label')
        else:
            column_names = ['username', 'profileImage', 'self_desc', 'label']
    else:
        if cross_features:
            column_names = ['feature{}'.format(i) for i in range(0, 36)]
            column_names.append('label')
        else:
            column_names = ['username', 'profileImage', 'self_desc', 'readability', 'post_text', 'uclassify', 'label']
    return column_names


def generate_dataset(data_list, mode, cross_features):
    data_dict = {'col{}'.format(x): data_list[x] for x in range(len(data_list))}
    column_names = __get_column_names(mode, cross_features)

    raw_dataset = pd.DataFrame.from_dict(data_dict, orient='index', columns=column_names)
    return raw_dataset.copy()


def generate_model(mode, cross_features=False):
    logger.info('Start generating model in {} mode.'.format('REALTIME' if mode == REALTIME_MODE else 'BATCH'))
    logger.info('Production of features {}.'.format('enabled' if cross_features else 'disabled'))
    items = Couch(DATABASE_LABELED_DATA).query_all()
    items = list(filter(lambda x: 'label' in x['vector'].keys(), items))
    logger.info('Retrieved {} labelled data from the database.'.format(len(items)))
    l = generate_feature_vectors(items, mode, cross_features)

    dataset = generate_dataset(l, mode, cross_features)
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_stats = train_dataset.describe()
    train_stats.pop("label")
    train_stats = train_stats.transpose()
    export_stats(train_stats, mode, cross_features)
    logger.info('Exported training stats.')

    train_labels = train_dataset.pop('label')
    test_labels = test_dataset.pop('label')

    normed_train_data = norm(train_dataset, train_stats)
    normed_test_data = norm(test_dataset, train_stats)

    model = build_model(train_dataset)

    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
    logger.info('Training...')
    history = model.fit(normed_train_data, train_labels, epochs=EPOCHS,
                        validation_split=0.2, verbose=0, callbacks=[early_stop, PrintDot()])
    print('')

    loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)
    logger.info("Evaluation of model:")
    logger.info("loss: {:5.2f}, mae: {:5.2f}, mse: {:5.2f}".format(loss, mae, mse))

    test_predictions = model.predict(normed_test_data).flatten()
    pred = [1.0 if x >= 0.5 else 0.0 for x in test_predictions]
    res = list(zip(test_labels, pred))
    tp = len(list(filter(lambda x: x[0] == 1 and x[1] == 1, res))) / len(list(filter(lambda x: x[0] == 1, res)))
    fp = len(list(filter(lambda x: x[0] == 0 and x[1] == 1, res))) / len(list(filter(lambda x: x[0] == 0, res)))
    tn = len(list(filter(lambda x: x[0] == 0 and x[1] == 0, res))) / len(list(filter(lambda x: x[0] == 0, res)))
    fn = len(list(filter(lambda x: x[0] == 1 and x[1] == 0, res))) / len(list(filter(lambda x: x[0] == 1, res)))
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    logger.info("Precision: {:5.4f}, Recall: {:5.4f}, F1-score: {:5.4f}".format(precision, recall, f1))

    return model


def export_stats(stats, mode, enable_crossfeature):
    json_data = stats.to_json()
    stat_name = _generate_stat_name(mode, enable_crossfeature)
    filename = MODEL_FILE_BASE_PATH + "{}.json".format(stat_name)
    if mode == REALTIME_MODE:
        Config(ALGOCONFIG_PATH).set('model-name/train-stats/realtime', "{}.json".format(stat_name))
    else:
        Config(ALGOCONFIG_PATH).set('model-name/train-stats/batch', "{}.json".format(stat_name))
    with open(filename, "w") as json_file:
        json_file.write(json_data)


def import_stats(filename):
    json_file = open(filename, 'r')
    data = json_file.read()
    json_file.close()
    logger.info('Loaded stats {}.'.format(filename))
    return pd.read_json(data)


class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0:
            print('')
        print('.', end='')


def _generate_model_name(mode, enable_crossfeature):
    date_str = date.today().strftime('%y%m%d')
    return "model_{}{}{}".format('realtime' if mode == REALTIME_MODE else 'batch', date_str,
                                 "cross" if enable_crossfeature else "")


def _generate_stat_name(mode, enable_crossfeature):
    date_str = date.today().strftime('%y%m%d')
    return "stat_{}{}{}".format('realtime' if mode == REALTIME_MODE else 'batch', date_str,
                                "cross" if enable_crossfeature else "")


def export_model(model, mode, enable_crossfeature):
    model_json = model.to_json(indent=2)
    model_name = _generate_model_name(mode, enable_crossfeature)
    jsonfile_path = MODEL_FILE_BASE_PATH + model_name + ".json"
    h5file_path = MODEL_FILE_BASE_PATH + model_name + ".h5"
    with open(jsonfile_path, "w") as json_file:
        json_file.write(model_json)
    model.save_weights(h5file_path)
    logger.info("Exporting model {} completed.".format(model_name))
    return model_name


def import_model(model_name):
    jsonfile_path = MODEL_FILE_BASE_PATH + "{}.json".format(model_name)
    h5file_path = MODEL_FILE_BASE_PATH + "{}.h5".format(model_name)
    json_file = open(jsonfile_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    _model = model_from_json(loaded_model_json)
    _model.load_weights(h5file_path)
    optimizer = tf.keras.optimizers.RMSprop(0.001)
    _model.compile(loss='mse',
                   optimizer=optimizer,
                   metrics=['mae', 'mse'])
    logger.info("Successfully loaded model {}.".format(model_name))
    return _model


def upgrade_model_batch():
    enable_crossfeature = Config(ALGOCONFIG_PATH).get('enable-cross-feature')
    _model = generate_model(REALTIME_MODE, cross_features=enable_crossfeature)
    model_name = export_model(_model, REALTIME_MODE, enable_crossfeature)
    Config(ALGOCONFIG_PATH).set('model-name/realtime', model_name)
    _model = generate_model(BATCH_MODE, cross_features=enable_crossfeature)
    model_name = export_model(_model, BATCH_MODE, enable_crossfeature)
    Config(ALGOCONFIG_PATH).set('model-name/batch', model_name)


if __name__ == '__main__':
    upgrade_model_batch()
