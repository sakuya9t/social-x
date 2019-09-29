from constant import BATCH_MODE
from similarity.SimCalculator import SimCalculator
from training.Sampler import Sampler
from utils import logger
from utils.QueryGenerator import retrieve


def generate(size, positive):
    dataset = Sampler().getPositiveDataset(size) if positive else Sampler().getNegativeDataset(size)
    calculator = SimCalculator()
    completed = 0
    for sample in dataset:
        account1 = {'platform': 'twitter', 'account': sample['twitter']}
        account2 = {'platform': 'instagram', 'account': sample['instagram']}
        try:
            logger.info('{} out of {} samples processed.'.format(completed, size))
            completed += 1
            data1 = retrieve(account1, BATCH_MODE)
            data2 = retrieve(account2, BATCH_MODE)
            fetch_result = calculator.fetch_vector(data1, data2)
            if len(fetch_result) > 0:
                continue
            vector = (calculator.vectorize(data1, data2, BATCH_MODE))
            vector['label'] = 1 if positive else 0
            calculator.store_result(data1, data2, vector)
        except Exception as ex:
            logger.error('Error: {}, account1: {}, account2: {}'.format(ex, account1, account2))
            continue
