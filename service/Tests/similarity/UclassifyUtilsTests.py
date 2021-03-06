import unittest

from similarity.UclassifyUtils import uclassify_topics, uclassify_similarity, generate_uclassify_key


class UclassifyUtilsTests(unittest.TestCase):
    def test_uclassify_topics(self):
        text = "Hellö Wörld@Python/?23$%67asdfjkl;[]}{\\';gasdfhjkl"
        result = uclassify_topics(text)
        self.assertTrue(len(result.keys()) > 0)

    def test_uclassify_similarity(self):
        text1 = 'Welcome! Are you completely new to programming? If not then we presume you will be looking for information about why and how to get started with Python.'
        text2 = 'Before getting started, you may want to find out which IDEs and text editors are tailored to make Python editing easy, browse the list of introductory books, or look at code samples that you might find helpful.'
        score = uclassify_similarity(text1, text2)
        self.assertTrue(0 <= score <= 1)

    def test_generate_key(self):
        api_key = generate_uclassify_key()
        self.assertTrue(isinstance(api_key, str))


if __name__ == '__main__':
    unittest.main()
