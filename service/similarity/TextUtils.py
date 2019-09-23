import ast
import re
import string
import urllib.parse
import numpy as np
import requests
import textdistance
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from urlextract import URLExtract
from constant import CONFIG_PATH
from similarity.Config import Config
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
import tensorflow as tf
import tensorflow_hub as hub


class TensorSimilarity:
    def __init__(self):
        self.initialize()

    def initialize(self):
        module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
        embed = hub.Module(module_url)
        self.session = tf.compat.v1.Session()
        self.session.run([tf.compat.v1.global_variables_initializer(), tf.compat.v1.tables_initializer()])
        self.similarity_input_placeholder = tf.compat.v1.placeholder(tf.string, shape=None)
        self.similarity_message_encodings = embed(self.similarity_input_placeholder)

    def similarity(self, msg1, msg2):
        # GUSE similarity
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


def uclassify_similarity(text1, text2):
    topics1 = uclassify_topics(text1)
    topics2 = uclassify_topics(text2)
    keys = set().union(topics1, topics2)
    vec1 = [topics1.get(key, 0) for key in keys]
    vec2 = [topics2.get(key, 0) for key in keys]
    return cosine_similarity([vec1], [vec2])[0][0]


def uclassify_topics(text):
    key = Config(CONFIG_PATH).get('uclassify/apikey')
    text = urllib.parse.quote_plus(text)
    url = 'https://api.uclassify.com/v1/uclassify/topics/classify?readkey={key}&text={text}'\
        .format(key=key, text=text)
    response = requests.get(url).text
    return ast.literal_eval(response)


def intersection(lst1, lst2):
    return set(lst1).intersection(lst2)


def extract_urls(text):
    return [re.sub(r'https?\/\/', '', x.lower()) for x in URLExtract().find_urls(text)]


def _get_default_url(platform, username):
    if platform in ['instagram', 'twitter', 'pinterest']:
        return [x.lower() for x in ['{}.com/{}'.format(platform, username), 'www.{}.com/{}'.format(platform, username),
                '{}.com/{}/'.format(platform, username), 'www.{}.com/{}/'.format(platform, username)]]
    elif platform == 'flickr':
        return [x.lower() for x in ['flickr.com/people/{}'.format(username), 'www.flickr.com/people/{}'.format(username),
                'flickr.com/people/{}/'.format(username), 'www.flickr.com/people/{}/'.format(username)]]


def desc_overlap_url(info1, info2):
    url_1 = extract_urls(info1['desc'])
    url_2 = extract_urls(info2['desc'])
    url_1 += _get_default_url(info1['platform'], info1['username'])
    url_2 += _get_default_url(info2['platform'], info2['username'])
    return 1 if len(intersection(url_1, url_2)) > 0 else 0


if __name__ == '__main__':
    str1 = 'TensorFlow Hub is a library for the publication, discovery, and consumption of reusable parts of machine learning models.'
    str2 = 'In the process of using a module from an URL there are many errors that can show up due to the network stack. Often this is a problem specific to the machine running the code and not an issue with the library.'
    print(similarity(str1, str2, 'jaccard'))
    print(similarity(str1, str2, 'sorensen'))
    tensorsim = TensorSimilarity()
    print(tensorsim.similarity(str1, str2))
