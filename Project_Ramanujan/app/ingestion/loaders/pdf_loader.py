from langchain_community.document_loaders import PyPDFLoader

class PDFLoaderWrapper:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        loader = PyPDFLoader(self.file_path)
        return loader.load()

'''
loader_instance = PDFLoaderWrapper(
    r"C:\Users\p.shivaji.pawar\Desktop\Priyanka\Personal_coding\Portfolio_Projects\Project_Ramanujan\data\raw\Books\Designing_ML_Systems.pdf"
)

documents=loader_instance.load()

print(f"Loaded {len(documents)} documents from the PDF file.")
print(documents[2])


import os

print("Current directory:", os.getcwd())
print("File exists:", os.path.exists(loader_instance.file_path))
print("Path:", loader_instance.file_path)
'''