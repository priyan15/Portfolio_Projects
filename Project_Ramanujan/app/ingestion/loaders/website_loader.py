from langchain_community.document_loaders import WebsiteLoader

class WebsiteLoaderWrapper:
    def __init__(self, url):
        self.url = url

    def load(self):
        loader = WebsiteLoader(self.url)
        return loader.load()