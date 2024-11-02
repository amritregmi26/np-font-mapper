import pymupdf

class FileHanlder:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def load_and_extract(self):
        with pymupdf.open(self.file_path) as doc:
            content = "".join([page.get_text() for page in doc])
        return content