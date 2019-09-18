import unittest

from similarity.TeaUtils import query_writing_style, writing_style_similarity, multi_thread_query_writing_style


class TeaUtilsTests(unittest.TestCase):

    def test_get_writing_style_scores(self):
        text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        metrics = query_writing_style(text=text)
        self.assertTrue('tea' not in metrics.keys())
        self.assertTrue('readbility' in metrics.keys())

    def test_tea_similarity(self):
        text1 = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        text2 = "How is it possible to adapt this code if the similarity has to be calculated within a matrix and not for two vectors? I thought I take a matrix and the transposed matrix instead of the second vector, bit it doesn't seem to work. "
        vec1 = query_writing_style(text1)
        vec2 = query_writing_style(text2)
        sim = writing_style_similarity(vec1, vec2)
        self.assertTrue(len(sim) == 1)
        self.assertTrue(all([0 <= x <= 1 for x in sim]))

    def test_multithread_get_writing_style_scores(self):
        text1 = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        text2 = "How is it possible to adapt this code if the similarity has to be calculated within a matrix and not for two vectors? I thought I take a matrix and the transposed matrix instead of the second vector, bit it doesn't seem to work. "
        metrics = multi_thread_query_writing_style([text1, text2], n_threads=2)
        self.assertTrue(len(metrics) == 2)
