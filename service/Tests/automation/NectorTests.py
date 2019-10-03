import unittest

from automation.Nectar import Nectar


class NectarTests(unittest.TestCase):
    def test_create_instance(self):
        nectar = Nectar()
        instance_info = nectar.add_instance()
        print(instance_info)


if __name__ == '__main__':
    unittest.main()
