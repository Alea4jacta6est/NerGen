import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from spacy.lang.en.stop_words import STOP_WORDS
import re


class Stopwords:
    def __init__(self, dir_="custom_stopwords"):
        self.dir_ = dir_
        self.spacy_stopwords = list(STOP_WORDS)
        self.nltk_stopwords = stopwords.words("english")
        self.custom_stopwords = []
        self.all_stopwords = self.get_all_stopwords()

    def get_more_stopwords(self, filename):
        file_path = f"{self.dir_}/{filename}"
        with open(file_path) as file:
            self.custom_stopwords = file.read().split("\n")[:-1]

    def get_all_stopwords(self):
        self.get_more_stopwords("stopwords.txt")
        all_ = set(self.custom_stopwords +
                   self.spacy_stopwords +
                   self.nltk_stopwords)
        return list(all_)


ALL_STOP_WORDS = Stopwords().all_stopwords


def form_corpus(texts: list):
    """
    Forming corpus based on texts and stopwords given
    :param texts:
    :return: corpus
    """
    lem = WordNetLemmatizer()
    corpus = []
    texts_amount = len(texts)
    for i in range(texts_amount):
        # Remove punctuation
        text = re.sub('[^a-zA-Z]', ' ', texts[i])
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and digits
        text = re.sub("(\\d|\\W)+", " ", text)
        # Convert to list from string
        text = text.split()
        # Lemmatize
        text = [lem.lemmatize(word) for word in text
                if word not in ALL_STOP_WORDS]
        text = " ".join(text)
        corpus.append(text)
    return corpus
