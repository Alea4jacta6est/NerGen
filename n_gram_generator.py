from sklearn.feature_extraction.text import CountVectorizer


# remove analyzer for english
def get_top_n_gram_words(corpus, n=None, gram=2):
    vec1 = CountVectorizer(ngram_range=(gram, gram),
                           max_features=20000, analyzer="char").fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                  vec1.vocabulary_.items()]
    words_freq = sorted(words_freq,
                        key=lambda x: x[1],
                        reverse=True)
    return words_freq[:n]
