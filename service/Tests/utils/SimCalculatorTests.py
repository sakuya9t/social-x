import unittest

from similarity.SimCalculator import SimCalculator


class SimCalculatorTests(unittest.TestCase):

    def test_create_calculator(self):
        calculator = SimCalculator()
        self.assertIsNotNone(calculator)
