import re
import string
import textdistance
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import tensorflow_hub as hub
import numpy as np


class TensorSimilarity:
    def __init__(self):
        self.initialize()

    def initialize(self):
        module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
        embed = hub.Module(module_url)
        self.session = tf.Session()
        self.session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        self.similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
        self.similarity_message_encodings = embed(self.similarity_input_placeholder)

    def similarity(self, msg1, msg2):
        messages = (msg1, msg2)
        message_embeddings = self.session.run(
            self.similarity_message_encodings, feed_dict={self.similarity_input_placeholder: messages})
        corr = np.inner(message_embeddings, message_embeddings)
        return corr.item((0, 1))

    def close(self):
        self.session.close()


def initialize():
    import nltk
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('stopwords')


def tokenize(text):
    text = text.lower()
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\x00-\x7F]','', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    tokens = word_tokenize(text)
    tokens = [x for x in tokens if len(x) > 1]
    tokens = [x for x in tokens if wordnet.synsets(x)]
    stop_words = set(stopwords.words('english'))
    tokens = [x for x in tokens if not x in stop_words]
    stemmer = PorterStemmer()
    tokens = list(map(lambda x: stemmer.stem(x), tokens))
    lemmatizer = WordNetLemmatizer()
    tokens = list(map(lambda x: lemmatizer.lemmatize(x), tokens))
    return tokens


def similarity(str1, str2, type):
    tokens_1 = tokenize(str1)
    tokens_2 = tokenize(str2)
    if type == 'jaccard':
        return textdistance.jaccard(tokens_1, tokens_2)
    elif type == 'sorensen':
        return textdistance.sorensen_dice(tokens_1, tokens_2)
    return 0


def singleword_similarity(profile1, profile2):
    keys = ['username', 'name', 'screen_name', 'full_name']
    res = -1
    for key1 in keys:
        for key2 in keys:
            if key1 in profile1.keys() and key2 in profile2.keys():
                res = max(res, textdistance.levenshtein.normalized_similarity(profile1[key1], profile2[key2]))
    return res


def topics_in_posts(posts):
    topics = []
    for post in posts:
        if '#' in post:
            matches = re.findall(r'#\w+', post)
            topics += matches
    return [x.replace('#', '') for x in topics]


def distinct_read(filename):
    s = set()
    with open(filename, "r") as file:
        line = file.readline()
        while line:
            s.add(line)
            line = file.readline()
    return s


def jaccard_counter_similarity(counter1, counter2):
    intersection = sum((counter1 & counter2).values())
    union = sum((counter1 | counter2).values())
    return 0 if union == 0 else intersection / union


if __name__ == '__main__':
    str1 = 'TensorFlow Hub is a library for the publication, discovery, and consumption of reusable parts of machine learning models.'
    str2 = 'In the process of using a module from an URL there are many errors that can show up due to the network stack. Often this is a problem specific to the machine running the code and not an issue with the library.'
    print(similarity(str1, str2, 'jaccard'))
    print(similarity(str1, str2, 'sorensen'))
    tensorsim = TensorSimilarity()
    print(tensorsim.similarity(str1, str2))
