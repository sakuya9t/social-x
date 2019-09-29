import unittest
from collections import Counter

from similarity.TextUtils import jaccard_counter_similarity, singleword_similarity, desc_overlap_url
from similarity.UclassifyUtils import uclassify_topics, uclassify_similarity


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


if __name__ == '__main__':
    unittest.main()
