import unittest

from training.Sampler import Sampler


class SamplerTests(unittest.TestCase):
    def test_generate_positive_samples(self):
        sample_size = 20
        dataset = Sampler().getPositiveDataset(sample_size)
        self.assertEqual(len(dataset), sample_size)

    def test_generate_negative_samples(self):
        sample_size = 20
        dataset = Sampler().getNegativeDataset(sample_size)
        self.assertEqual(len(dataset), sample_size)


if __name__ == '__main__':
    unittest.main()
