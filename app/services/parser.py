import fitz  # PyMuPDF
import docx
import os


class ResumeParser:

    @staticmethod
    def extract_text(file_path: str):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return ResumeParser.read_pdf(file_path)

        elif extension == ".docx":
            return ResumeParser.read_docx(file_path)

        return ""

    @staticmethod
    def read_pdf(file_path):

        text = ""

        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text

    @staticmethod
    def read_docx(file_path):

        document = docx.Document(file_path)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text