from datetime import date

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.python.keras.models import model_from_json

from utils import logger
from tensorflow import keras
from constant import REALTIME_MODE, BATCH_MODE, DATABASE_LABELED_DATA, MODEL_FILE_BASE_PATH
from utils.Couch import Couch

EPOCHS = 1000


def generate_model(mode, cross_features=False):
    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']

    def build_model():
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

    logger.info('Start generating model in {} mode.'.format('REALTIME' if mode == REALTIME_MODE else 'BATCH'))
    logger.info('Production of features {}.'.format('enabled' if cross_features else 'disabled'))
    items = Couch(DATABASE_LABELED_DATA).query_all()
    items = list(filter(lambda x: 'label' in x['vector'].keys(), items))
    logger.info('Retrieved {} labelled data from the database.'.format(len(items)))
    l = [[list([float(a) for a in x.values()]) if isinstance(x, dict) else [float(x)] for x in item['vector'].values()]
         for item in items]
    if mode == REALTIME_MODE:
        l = [x[0:3] + x[-1:] for x in l]
    else:
        l = [x[0:3] + x[4:] for x in l]
        l = list(filter(lambda x: len(x) == 7, l))

    if cross_features:
        if mode == REALTIME_MODE:
            l = [np.append(np.array(item[:-1]).dot(np.array(item[:-1]).reshape((1, 3))).flatten(), item[-1]) for item in
                 l]
        else:
            l = [np.append(np.array(item[:-1]).dot(np.array(item[:-1]).reshape((1, 6))).flatten(), item[-1]) for item in
                 l]
    else:
        l = [np.array(x).flatten() for x in l]

    data_dict = {'col{}'.format(x): l[x] for x in range(len(l))}
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

    raw_dataset = pd.DataFrame.from_dict(data_dict, orient='index', columns=column_names)
    dataset = raw_dataset.copy()
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_stats = train_dataset.describe()
    train_stats.pop("label")
    train_stats = train_stats.transpose()

    train_labels = train_dataset.pop('label')
    test_labels = test_dataset.pop('label')

    normed_train_data = norm(train_dataset)
    normed_test_data = norm(test_dataset)

    model = build_model()

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


class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0:
            print('')
        print('.', end='')


def export_model(model):
    model_json = model.to_json(indent=2)
    date_str = date.today().strftime('%y%m%d')
    jsonfile_path = MODEL_FILE_BASE_PATH + "model{}.json".format(date_str)
    h5file_path = MODEL_FILE_BASE_PATH + "model{}.h5".format(date_str)
    with open(jsonfile_path, "w") as json_file:
        json_file.write(model_json)
    model.save_weights(h5file_path)
    logger.info("Saved model to disk, files: {}, {}.".format(jsonfile_path, h5file_path))


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
