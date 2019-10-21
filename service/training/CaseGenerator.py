from constant import BATCH_MODE, DATABASE_LABELED_DATA
from similarity.SimCalculator import SimCalculator
from training.Sampler import Sampler
from utils import logger
from utils.QueryGenerator import retrieve


def generate(size, positive):
    dataset = Sampler().getPositiveDataset(size) if positive else Sampler().getNegativeDataset(size)
    calculator = SimCalculator()
    for index, sample in enumerate(dataset):
        account1 = {'platform': 'twitter', 'account': sample['twitter']}
        account2 = {'platform': 'instagram', 'account': sample['instagram']}
        try:
            logger.info('Processing {}-th sample. Account1: {}, Account2: {}.'.format(index, account1, account2))
            data1 = retrieve(account1, BATCH_MODE)
            data2 = retrieve(account2, BATCH_MODE)
            fetch_result = calculator.fetch_vector(data1, data2, DATABASE_LABELED_DATA)
            if len(fetch_result) > 0:
                continue
            vector = (calculator.calc(data1, data2, enable_networking=False, mode=BATCH_MODE))
            vector['label'] = 1 if positive else 0
            calculator.store_result(data1, data2, vector, DATABASE_LABELED_DATA)
        except Exception as ex:
            logger.error('Error: {}, account1: {}, account2: {}'.format(ex, account1, account2))
            continue
