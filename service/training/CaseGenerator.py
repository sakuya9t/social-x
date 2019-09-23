from constant import BATCH_MODE
from similarity.SimCalculator import SimCalculator
from training.Sampler import Sampler
from utils.QueryGenerator import retrieve


def generate(size, positive):
    dataset = Sampler().getPositiveDataset(size) if positive else Sampler().getNegativeDataset(size)
    calculator = SimCalculator()
    vectors = []
    for sample in dataset:
        data1 = retrieve(sample['twitter'], BATCH_MODE)
        data2 = retrieve(sample['instagram'], BATCH_MODE)
        vectors.append(calculator.vectorize(data1, data2, BATCH_MODE))
