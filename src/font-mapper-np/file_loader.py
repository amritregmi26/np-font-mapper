import pymupdf
import mimetypes

class FileHanlder:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def load_and_extract(self):
        # file_type = mimetypes.guess_type(self.file_path)
        with pymupdf.open(self.file_path) as doc:
            content = "".join([page.get_text() for page in doc])
        return content
    
    # def pdf_to_txt(self):
    #     pass