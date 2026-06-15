from pypdf import PdfReader


class PDFReader:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):

        reader = PdfReader(self.pdf_path)

        full_text = ""

        print(f"Total Pages: {len(reader.pages)}")

        for i, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text:
                full_text += text + "\n"

            print(f"Processed Page {i}")

        return full_text