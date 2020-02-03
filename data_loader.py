import os


class DataLoader:
    def __init__(self, dir_):
        self.dir_ = dir_
        self.list_files = os.listdir(self.dir_)
        self.texts = self.extract_texts_from_txt()

    def extract_texts_from_txt(self):
        texts = []
        for filename in self.list_files:
            with open(f"{self.dir_}/{filename}") as ff:
                text = ff.read()
                texts.append(text)
        return texts

