from langchain_community.document_loaders import UnstructuredMarkdownLoader

class MarkdownLoaderWrapper:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        loader = UnstructuredMarkdownLoader(self.file_path)
        return loader.load()