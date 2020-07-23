from itertools import chain
from pathlib import Path
from bs4 import BeautifulSoup
from tika import parser

PATTERNS = ["**/*.pdf", "**/*.txt", "*.txt"]


# TODO: add a feature to process pdf/txt in a folder and form a corpus
class DataLoader:
    def __init__(self, dir_to_files, nested=True):
        self.dir_ = dir_to_files
        self.list_files = Path(self.dir_).glob("**/*.txt") if nested else None
        self.group_ext = {k: [] for k in ["pdf", "txt"]}
        self.texts = self.extract_texts_from_txt()

    def extract_texts_from_txt(self):
        texts = []
        for file_path in self.list_files:
            with open(file_path) as ff:
                text = ff.read()
                texts.append(text)
        return texts

    def extract_texts_from_pdf(self):
        """Load a PDF file.

        Args:
            pdf (str, Path, binary file-object): PDF file.

        Returns:
            list: list of pages.
                Each page contains list of paragraphs.
        """
        # tika's parser requires only str-like paths
        if isinstance(self.dir_, Path):
            self.dir_ = str(self.dir_)
        if isinstance(self.dir_, str):
            parser_ = parser.from_file
        else:
            parser_ = parser.from_buffer

        parsed: BeautifulSoup = BeautifulSoup(
            parser_(self.dir_, xmlContent=True)["content"], features="lxml")

        list_of_pages = []
        for div in parsed.find_all("div", {"class": "page"}):
            list_of_paragraphs = []
            for p in div.find_all("p"):
                par = p.text.replace("-\n", "").replace("\n", "")
                if par:
                    list_of_paragraphs.append(par)
            list_of_pages.append(list_of_paragraphs)
        return list(chain(*list_of_pages))
