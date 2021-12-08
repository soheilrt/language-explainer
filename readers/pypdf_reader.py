from io import StringIO
import PyPDF2
from models.reader import Reader


class PyPDFReader(Reader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.file = open(file_path, 'rb')

    def __del__(self):
        self.file.close()

    def read(self) -> str:
        pdf_text_buffer = StringIO()
        pdf_reader = PyPDF2.PdfFileReader(self.file)

        num_pages = pdf_reader.getNumPages()

        for index in range(num_pages):
            pdf_text_buffer.write(pdf_reader.getPage(index).extractText())

        return pdf_text_buffer.getvalue()
