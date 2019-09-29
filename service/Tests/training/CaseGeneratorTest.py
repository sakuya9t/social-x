import unittest

from training.CaseGenerator import generate

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)


class CaseGeneratorTest(unittest.TestCase):
    def test_generate_positive(self):
        generate(50, positive=True)

    def test_generate_negative(self):
        generate(50, positive=False)


if __name__ == '__main__':
    unittest.main()
