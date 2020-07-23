import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from spacy.lang.en.stop_words import STOP_WORDS
from string import ascii_letters
from pathlib import Path
import re

STOPWORD_FILENAMES = {"en": "en_stopwords.txt",
                      "zh": "zh_stopwords.txt",
                      "fr": "fr_stopwords.txt"}


class Stopwords:
    def __init__(self, lang, dir_="custom_stopwords"):
        self.dir_ = dir_
        self.spacy_stopwords = list(STOP_WORDS)
        self.nltk_stopwords = stopwords.words("english")
        self.custom_stopwords_path = STOPWORD_FILENAMES[lang]
        self.custom_stopwords = []
        self.all_stopwords = self.get_all_stopwords()

    def get_custom_stopwords(self):
        file_path = f"{self.dir_}/{self.custom_stopwords_path}"
        with open(file_path) as file:
            self.custom_stopwords = file.read().split("\n")[:-1]

    def get_all_stopwords(self):
        self.get_custom_stopwords()
        all_ = set(self.custom_stopwords +
                   self.spacy_stopwords +
                   self.nltk_stopwords)
        return list(all_)


def form_corpus(texts: list, lang: str):
    """
    Forming corpus based on texts and stopwords given

    Args:
     texts: list
     lang: str

    Returns:
     corpus: list of texts
    """
    ALL_STOP_WORDS = Stopwords(lang).all_stopwords
    corpus = []
    if lang == "zh":
        for i, text in enumerate(texts):
            # Remove special characters and digits
            text = re.sub("(\\d|\\W)+", "", text)
            text_ = [char for char in text if char not in ALL_STOP_WORDS and char not in ascii_letters]
            text_ = "".join(text_)
            corpus.append(text_)
    else:
        lem = WordNetLemmatizer()
        for i, text in enumerate(texts):
            # Remove punctuation
            text_ = re.sub('[^a-zA-Z]', ' ', text)
            # Convert to lowercase
            text_ = text_.lower()
            # Remove special characters and digits
            text_ = re.sub("(\\d|\\W)+", " ", text_)
            # Convert to list from string
            text_ = text_.split()
            # Lemmatize
            text_ = [lem.lemmatize(word) for word in text_
                    if word not in ALL_STOP_WORDS]
            text_ = " ".join(text_)
            corpus.append(text_)
    return corpus
