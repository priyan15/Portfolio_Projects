from langchain_community.document_loaders import TextLoader

class TextLoaderWrapper:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        loader = TextLoader(self.file_path)
        return loader.load()