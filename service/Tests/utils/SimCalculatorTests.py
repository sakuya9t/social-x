import unittest

from similarity.SimCalculator import SimCalculator


class SimCalculatorTests(unittest.TestCase):
    driver = '../../chromedriver'

    def test_create_calculator(self):
        calculator = SimCalculator(driver=self.driver, config='../../algomodule.config')
        self.assertIsNotNone(calculator)
