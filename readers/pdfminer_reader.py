from models.reader import Reader
from pdfminer.high_level import extract_text


class PDFMinerReader(Reader):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def read(self) -> str:
        print("reading file: " + self.file_path)
        return extract_text(self.file_path)
