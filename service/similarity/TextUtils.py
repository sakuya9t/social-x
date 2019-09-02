import re
import string
import textdistance
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


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


def similarity(str1, str2):
    tokens_1 = tokenize(str1)
    tokens_2 = tokenize(str2)
    return [textdistance.jaccard(tokens_1, tokens_2), textdistance.sorensen_dice(tokens_1, tokens_2)]


def distinct_read(filename):
    s = set()
    with open(filename, "r") as file:
        line = file.readline()
        while line:
            s.add(line)
            line = file.readline()
    return s
