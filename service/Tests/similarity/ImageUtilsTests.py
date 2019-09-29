import unittest

from similarity.ImageUtils import Mrisa


class TextUtilsTests(unittest.TestCase):
    def test_mrisa_function(self):
        mrisa = Mrisa()
        url = 'https://images-na.ssl-images-amazon.com/images/I/51GUL1MtK7L._SL1000_.jpg'
        image_info = mrisa.get_image_info(url)
        expected_keys = ['links', 'descriptions', 'titles', 'similar_images', 'best_guess']
        self.assertTrue(isinstance(image_info, dict))
        for key in expected_keys:
            self.assertTrue(key in image_info.keys())

    def test_mrisa_create_service_function_terminate(self):
        mrisa = Mrisa()
        mrisa.start()
        url = 'https://images-na.ssl-images-amazon.com/images/I/51GUL1MtK7L._SL1000_.jpg'
        image_info = mrisa.get_image_info(url)
        expected_keys = ['links', 'descriptions', 'titles', 'similar_images', 'best_guess']
        self.assertTrue(isinstance(image_info, dict))
        for key in expected_keys:
            self.assertTrue(key in image_info.keys())
        mrisa.stop()


if __name__ == '__main__':
    unittest.main()
