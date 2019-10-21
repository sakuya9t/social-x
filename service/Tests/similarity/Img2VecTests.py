import unittest

from similarity.ImageUtils import Mrisa, load_image
from similarity.img_to_vec import Img2Vec


class Img2VecTests(unittest.TestCase):
    def test_picture_1(self):
        url = 'https://s.pinimg.com/images/user/default_280.png'
        img = load_image(url)
        vec = Img2Vec().get_vec(img)
        print(vec)


if __name__ == '__main__':
    unittest.main()
