from corpus_builder import form_corpus
from n_gram_generator import get_top_n_gram_words
from data_loader import DataLoader
import pandas as pd
import argparse
import os

OUTPUT_DIR = "grams"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

parser = argparse.ArgumentParser(description='Process texts to get n-grams')
parser.add_argument('-p', '--path_to_folder', type=str,
                    help='path that leads to a folder with txt files')
parser.add_argument('-g', '--n_grams', nargs='+', type=int, default=[1, 2, 3],
                    help='n-grams parameter to get most frequent entities')
parser.add_argument('-s', '--size', type=int, default=20,
                    help='parameter limiting the amount of entities generated')
parser.add_argument('-c', '--to_csv', type=bool, default=True,
                    help='parameter controlling csv creation')

args = parser.parse_args()
texts = DataLoader(args.path_to_folder).texts
corpus = form_corpus(texts)

for num in args.n_grams:
    top_words = get_top_n_gram_words(corpus, n=args.size, gram=num)
    if str(args.to_csv).upper() == "TRUE":
        df = pd.DataFrame(top_words, columns=["Entity", "Frequency"])
        df.to_csv(f"{OUTPUT_DIR}/{num}-gram.csv", index=False)
