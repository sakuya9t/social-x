import os
import unittest

from training.Sampler import Sampler, CONFIG, INSTA_FOLDER, TWITTER_FOLDER


class SamplerTests(unittest.TestCase):
    def test_generate_positive_samples(self):
        sample_size = 20
        dataset = Sampler().getPositiveDataset(sample_size)
        for item in dataset:
            ins_path = INSTA_FOLDER + "{}.txt".format(item['instagram'])
            twi_path = TWITTER_FOLDER + "{}.txt".format(item['twitter'])
            self.assertTrue(os.path.exists(ins_path) and os.path.exists(twi_path))

    def test_generate_negative_samples(self):
        sample_size = 20
        dataset = Sampler().getNegativeDataset(sample_size)
        for item in dataset:
            ins_path = INSTA_FOLDER + "{}.txt".format(item['instagram'])
            twi_path = TWITTER_FOLDER + "{}.txt".format(item['twitter'])
            self.assertTrue(os.path.exists(ins_path) and os.path.exists(twi_path))


if __name__ == '__main__':
    unittest.main()
